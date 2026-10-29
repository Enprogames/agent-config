"""Approval-gated, exact-printer PDF submission for Windows."""

from __future__ import annotations

import ctypes
import hashlib
import hmac
import json
import os
import re
import secrets
import subprocess
from ctypes import wintypes
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from scripts.response_pdf.errors import PrintError
from scripts.response_pdf.paths import SETTINGS_PATH, SUMATRA_PATH
from scripts.response_pdf.verification import load_verified_manifest, sha256_file

SAFE_SETTINGS = re.compile(r"^[A-Za-z0-9=., x-]+$")
PRINTER_ENUM_LOCAL = 0x00000002
PRINTER_ENUM_CONNECTIONS = 0x00000004


class _PrinterInfo2(ctypes.Structure):
    _fields_ = [
        ("pServerName", wintypes.LPWSTR),
        ("pPrinterName", wintypes.LPWSTR),
        ("pShareName", wintypes.LPWSTR),
        ("pPortName", wintypes.LPWSTR),
        ("pDriverName", wintypes.LPWSTR),
        ("pComment", wintypes.LPWSTR),
        ("pLocation", wintypes.LPWSTR),
        ("pDevMode", wintypes.LPVOID),
        ("pSepFile", wintypes.LPWSTR),
        ("pPrintProcessor", wintypes.LPWSTR),
        ("pDatatype", wintypes.LPWSTR),
        ("pParameters", wintypes.LPWSTR),
        ("pSecurityDescriptor", wintypes.LPVOID),
        ("Attributes", wintypes.DWORD),
        ("Priority", wintypes.DWORD),
        ("DefaultPriority", wintypes.DWORD),
        ("StartTime", wintypes.DWORD),
        ("UntilTime", wintypes.DWORD),
        ("Status", wintypes.DWORD),
        ("cJobs", wintypes.DWORD),
        ("AveragePPM", wintypes.DWORD),
    ]


def _settings() -> dict[str, Any]:
    try:
        value = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PrintError(f"Invalid skill settings: {exc}") from exc
    if not isinstance(value, dict):
        raise PrintError("Skill settings must be a JSON object.")
    return value


def list_printers() -> list[dict[str, Any]]:
    """Enumerate Windows printers without changing printer state."""
    if os.name != "nt":
        raise PrintError("Physical printing is currently implemented only for Windows.")
    winspool = ctypes.WinDLL("winspool.drv", use_last_error=True)
    enum_printers = winspool.EnumPrintersW
    enum_printers.argtypes = [
        wintypes.DWORD,
        wintypes.LPWSTR,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.BYTE),
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        ctypes.POINTER(wintypes.DWORD),
    ]
    enum_printers.restype = wintypes.BOOL
    flags = PRINTER_ENUM_LOCAL | PRINTER_ENUM_CONNECTIONS
    needed = wintypes.DWORD(0)
    returned = wintypes.DWORD(0)
    enum_printers(flags, None, 2, None, 0, ctypes.byref(needed), ctypes.byref(returned))
    if needed.value == 0:
        return []
    buffer = ctypes.create_string_buffer(needed.value)
    byte_buffer = ctypes.cast(buffer, ctypes.POINTER(wintypes.BYTE))
    if not enum_printers(
        flags,
        None,
        2,
        byte_buffer,
        needed,
        ctypes.byref(needed),
        ctypes.byref(returned),
    ):
        error = ctypes.WinError(ctypes.get_last_error())
        raise PrintError(f"Could not enumerate printers: {error}")
    records = ctypes.cast(buffer, ctypes.POINTER(_PrinterInfo2))
    return [
        {
            "Name": records[index].pPrinterName or "",
            "DriverName": records[index].pDriverName or "",
            "PortName": records[index].pPortName or "",
            "PrinterStatus": records[index].Status,
        }
        for index in range(returned.value)
    ]


def _windows_default_printer_name() -> str:
    """Return the single printer currently marked as the Windows default."""
    if os.name != "nt":
        raise PrintError("Physical printing is currently implemented only for Windows.")
    winspool = ctypes.WinDLL("winspool.drv", use_last_error=True)
    get_default_printer = winspool.GetDefaultPrinterW
    get_default_printer.argtypes = [wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
    get_default_printer.restype = wintypes.BOOL
    size = wintypes.DWORD(0)
    get_default_printer(None, ctypes.byref(size))
    if size.value == 0:
        raise PrintError(
            "Windows did not report a default printer. "
            "Specify the printer explicitly with --printer."
        )
    buffer = ctypes.create_unicode_buffer(size.value)
    if not get_default_printer(buffer, ctypes.byref(size)):
        error = ctypes.WinError(ctypes.get_last_error())
        raise PrintError(f"Could not determine the Windows default printer: {error}")
    name = buffer.value.strip()
    if not name:
        raise PrintError(
            "Windows returned an empty default printer name. "
            "Specify the printer explicitly with --printer."
        )
    return name


def _select_printer_name(
    settings: dict[str, Any], requested_name: str | None
) -> tuple[str, str]:
    """Select an explicit printer or resolve the configured printer policy."""
    if requested_name and requested_name.strip():
        return requested_name.strip(), "explicit"
    policy = str(settings.get("printer_policy", ""))
    if policy == "windows-default":
        return _windows_default_printer_name(), "windows-default"
    raise PrintError(
        f"Unsupported or missing printer policy {policy!r}. "
        "Specify the printer explicitly with --printer."
    )


def _resolve_printer(name: str) -> dict[str, Any]:
    matches = [
        printer
        for printer in list_printers()
        if str(printer.get("Name", "")).casefold() == name.casefold()
    ]
    if len(matches) != 1:
        available = ", ".join(str(item.get("Name")) for item in list_printers())
        raise PrintError(
            f"Printer {name!r} was not found uniquely. Installed printers: {available}"
        )
    return matches[0]


def _assert_printer_identity(
    planned_printer: dict[str, Any], current_printer: dict[str, Any]
) -> None:
    """Require the approved printer name, driver, and port to remain unchanged."""
    fields = ("Name", "DriverName", "PortName")
    changed = [
        field
        for field in fields
        if str(planned_printer.get(field, "")).casefold()
        != str(current_printer.get(field, "")).casefold()
    ]
    if changed:
        raise PrintError(
            "Printer identity changed after the print plan was prepared "
            f"({', '.join(changed)}). Prepare a new plan and approve it."
        )


def _assert_plan_integrity(plan: dict[str, Any]) -> None:
    recorded = str(plan.get("plan_sha256", ""))
    unsigned = dict(plan)
    unsigned.pop("plan_sha256", None)
    canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":"))
    calculated = hashlib.sha256(canonical.encode()).hexdigest()
    if not hmac.compare_digest(recorded, calculated):
        raise PrintError("Print plan changed after it was prepared.")


def _confirmation_text(
    pdf_name: str,
    page_count: int,
    printer: dict[str, Any],
    printer_source: str,
    print_settings: str,
) -> str:
    source_description = (
        "Windows default when this plan was prepared"
        if printer_source == "windows-default"
        else "explicitly selected"
    )
    return (
        f"PRINT CONFIRMATION - PRINTER: {printer['Name']!r} "
        f"({source_description}; driver: {printer.get('DriverName')!r}; "
        f"port: {printer.get('PortName')!r}). JOB: 1 copy of {pdf_name} "
        f"({page_count} page(s)); settings: {print_settings!r}. "
        "Approve this exact job or specify a different printer/settings."
    )


def prepare_print(
    manifest_path: Path,
    plan_path: Path,
    printer_name: str | None,
    print_settings: str | None,
) -> dict[str, Any]:
    """Create a time-limited plan for later user-approved submission."""
    manifest = load_verified_manifest(manifest_path.resolve())
    settings = _settings()
    printer_name, printer_source = _select_printer_name(settings, printer_name)
    print_settings = print_settings or str(
        settings.get("default_print_settings", "1x,fit,paper=letter")
    )
    if not SAFE_SETTINGS.fullmatch(print_settings):
        raise PrintError("Print settings contain unsupported characters.")
    printer = _resolve_printer(printer_name)
    approval_code = secrets.token_hex(4).upper()
    created_at = datetime.now(UTC)
    ttl = int(settings.get("approval_ttl_minutes", 30))
    pdf = Path(manifest["pdf_path"])
    plan = {
        "format_version": 1,
        "created_at": created_at.isoformat(),
        "expires_at": (created_at + timedelta(minutes=ttl)).isoformat(),
        "manifest_path": str(manifest_path.resolve()),
        "pdf_path": str(pdf),
        "pdf_sha256": manifest["pdf_sha256"],
        "page_count": manifest["page_count"],
        "printer": printer,
        "printer_source": printer_source,
        "print_settings": print_settings,
        "approval_code": approval_code,
        "print_engine": str(SUMATRA_PATH),
    }
    canonical = json.dumps(plan, sort_keys=True, separators=(",", ":"))
    plan["plan_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    plan_path = plan_path.resolve()
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    plan["plan_path"] = str(plan_path)
    plan["confirmation"] = _confirmation_text(
        pdf.name,
        manifest["page_count"],
        printer,
        printer_source,
        print_settings,
    )
    return plan


def execute_print(
    plan_path: Path, approval_code: str, *, validate_only: bool = False
) -> dict[str, Any]:
    """Validate a plan and, unless requested otherwise, submit exactly one job."""
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PrintError(f"Invalid print plan: {exc}") from exc
    _assert_plan_integrity(plan)
    expected_code = str(plan.get("approval_code", ""))
    if not hmac.compare_digest(expected_code, approval_code):
        raise PrintError("Approval code does not match this print plan.")
    expires_at = datetime.fromisoformat(str(plan.get("expires_at")))
    if datetime.now(UTC) > expires_at:
        raise PrintError("Print approval plan has expired. Prepare a new plan.")
    load_verified_manifest(Path(plan["manifest_path"]))
    pdf = Path(plan["pdf_path"])
    if sha256_file(pdf) != plan.get("pdf_sha256"):
        raise PrintError("PDF changed after the print plan was prepared.")
    planned_printer = plan.get("printer", {})
    if not isinstance(planned_printer, dict):
        raise PrintError("Print plan does not contain a valid printer identity.")
    printer_name = str(planned_printer.get("Name", ""))
    current_printer = _resolve_printer(printer_name)
    _assert_printer_identity(planned_printer, current_printer)
    if not SUMATRA_PATH.is_file():
        raise PrintError(f"Pinned print engine is missing: {SUMATRA_PATH}")
    if validate_only:
        return {
            "status": "validated-not-printed",
            "pdf": str(pdf),
            "printer": printer_name,
        }
    command = [
        str(SUMATRA_PATH),
        "-silent",
        "-print-to",
        printer_name,
        "-print-settings",
        str(plan["print_settings"]),
        str(pdf),
    ]
    completed = subprocess.run(command, check=False, timeout=120)
    if completed.returncode:
        meanings = {
            2: "could not open the PDF",
            3: "the PDF disallows printing",
            4: "printer not found",
            5: "printer driver or device failure",
            6: "printing disabled by policy",
        }
        detail = meanings.get(completed.returncode, "unknown print engine failure")
        raise PrintError(f"Print submission failed: {detail} ({completed.returncode}).")
    return {
        "status": "submitted-to-windows-spooler",
        "pdf": str(pdf),
        "printer": printer_name,
    }
