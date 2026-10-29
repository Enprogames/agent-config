"""Unit tests for invariant-preserving helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.response_pdf.codex_capture import _last_final_answer
from scripts.response_pdf.errors import CaptureError, PrintError, VerificationError
from scripts.response_pdf.printing import (
    _assert_plan_integrity,
    _assert_printer_identity,
    _confirmation_text,
    _select_printer_name,
)
from scripts.response_pdf.verification import (
    _expected_external_links,
    load_verified_manifest,
    sha256_file,
)


def test_selects_latest_final_answer_only() -> None:
    thread = {
        "turns": [
            {
                "items": [
                    {"type": "agentMessage", "phase": "commentary", "text": "work"},
                    {"type": "agentMessage", "phase": "final_answer", "text": "first"},
                ]
            },
            {
                "items": [
                    {"type": "userMessage", "content": []},
                    {"type": "agentMessage", "phase": "commentary", "text": "more"},
                    {"type": "agentMessage", "phase": "final_answer", "text": "second"},
                ]
            },
        ]
    }
    assert _last_final_answer(thread) == "second"


def test_capture_requires_a_final_answer() -> None:
    with pytest.raises(CaptureError):
        _last_final_answer(
            {"turns": [{"items": [{"type": "agentMessage", "text": ""}]}]}
        )


def test_manifest_detects_pdf_mutation(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    pdf = tmp_path / "out.pdf"
    source.write_bytes(b"exact\n")
    pdf.write_bytes(b"pdf-one")
    manifest = {
        "source_path": str(source),
        "source_sha256": sha256_file(source),
        "pdf_path": str(pdf),
        "pdf_sha256": sha256_file(pdf),
        "verification": "passed",
    }
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    pdf.write_bytes(b"pdf-two")
    with pytest.raises(VerificationError, match="PDF changed"):
        load_verified_manifest(path)


def test_utf8_hash_is_byte_exact(tmp_path: Path) -> None:
    value = "alpha\nβeta\n```python\nprint('x')\n```\n"
    path = tmp_path / "source.md"
    path.write_bytes(value.encode("utf-8"))
    assert sha256_file(path) == hashlib.sha256(value.encode("utf-8")).hexdigest()


def test_print_plan_detects_mutation() -> None:
    plan = {"approval_code": "A1B2C3D4", "printer": {"Name": "Printer A"}}
    canonical = json.dumps(plan, sort_keys=True, separators=(",", ":"))
    plan["plan_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    _assert_plan_integrity(plan)
    plan["printer"] = {"Name": "Printer B"}
    with pytest.raises(PrintError, match="changed"):
        _assert_plan_integrity(plan)


def test_explicit_printer_overrides_default_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_called() -> str:
        raise AssertionError("Windows default must not be queried")

    monkeypatch.setattr(
        "scripts.response_pdf.printing._windows_default_printer_name",
        fail_if_called,
    )
    assert _select_printer_name(
        {"printer_policy": "windows-default"}, " Printer A "
    ) == ("Printer A", "explicit")


def test_windows_default_policy_records_its_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "scripts.response_pdf.printing._windows_default_printer_name",
        lambda: "Printer A",
    )
    assert _select_printer_name({"printer_policy": "windows-default"}, None) == (
        "Printer A",
        "windows-default",
    )


def test_missing_printer_policy_requires_explicit_printer() -> None:
    with pytest.raises(PrintError, match="Specify the printer explicitly"):
        _select_printer_name({}, None)


def test_printer_identity_detects_driver_or_port_change() -> None:
    planned = {"Name": "Printer A", "DriverName": "Driver A", "PortName": "PORT1"}
    _assert_printer_identity(planned, dict(planned))
    changed = dict(planned, PortName="PORT2")
    with pytest.raises(PrintError, match="Printer identity changed"):
        _assert_printer_identity(planned, changed)


def test_confirmation_makes_resolved_default_printer_obvious() -> None:
    confirmation = _confirmation_text(
        "document.pdf",
        2,
        {
            "Name": "Printer A",
            "DriverName": "Driver A",
            "PortName": "PORT1",
        },
        "windows-default",
        "1x,fit,paper=letter",
    )
    assert "PRINTER: 'Printer A'" in confirmation
    assert "Windows default when this plan was prepared" in confirmation
    assert "driver: 'Driver A'" in confirmation
    assert "port: 'PORT1'" in confirmation
    assert "1 copy of document.pdf (2 page(s))" in confirmation


def test_external_link_selection_excludes_relative_targets() -> None:
    markdown = (
        "[web](https://example.com) [mail](mailto:a@example.com) [local](file.md)"
    )
    assert _expected_external_links(markdown) == [
        "https://example.com",
        "mailto:a@example.com",
    ]
