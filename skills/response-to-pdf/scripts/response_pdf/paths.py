"""Stable skill paths and executable discovery."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = SKILL_ROOT / "assets"
SETTINGS_PATH = SKILL_ROOT / "settings.json"
SUMATRA_INSTALL_COMMAND = "winget install --id SumatraPDF.SumatraPDF --exact"
# The mermaid skill, installed beside this one, owns the pinned Mermaid bundle.
MERMAID_BUNDLE = SKILL_ROOT.parent / "mermaid" / "assets" / "mermaid.min.js"


def find_edge() -> Path:
    """Return a usable Chromium-based Microsoft Edge executable."""
    configured = os.environ.get("RESPONSE_PDF_BROWSER")
    candidates = [
        Path(configured) if configured else None,
        Path(os.environ.get("PROGRAMFILES(X86)", ""))
        / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("PROGRAMFILES", ""))
        / "Microsoft/Edge/Application/msedge.exe",
    ]
    for candidate in candidates:
        if candidate and candidate.is_file():
            return candidate.resolve()
    discovered = shutil.which("msedge") or shutil.which("chrome")
    if discovered:
        return Path(discovered).resolve()
    message = (
        "No supported Chromium browser was found. Install Microsoft Edge or set "
        "RESPONSE_PDF_BROWSER to its executable."
    )
    raise FileNotFoundError(message)


def find_sumatra() -> Path:
    """Return the installed SumatraPDF executable used to submit print jobs."""
    configured = os.environ.get("RESPONSE_PDF_SUMATRA")
    if configured:
        if Path(configured).is_file():
            return Path(configured).resolve()
        message = f"RESPONSE_PDF_SUMATRA does not name a file: {configured}"
        raise FileNotFoundError(message)
    discovered = shutil.which("SumatraPDF")
    # winget's per-machine and per-user installation directories.
    install_roots = [os.environ.get("PROGRAMFILES"), os.environ.get("LOCALAPPDATA")]
    candidates = [Path(discovered)] if discovered else []
    candidates += [
        Path(root) / "SumatraPDF/SumatraPDF.exe" for root in install_roots if root
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    message = (
        "SumatraPDF is required for printing and was not found. Ask the user to "
        f"install it with `{SUMATRA_INSTALL_COMMAND}`, or set RESPONSE_PDF_SUMATRA "
        "to its executable."
    )
    raise FileNotFoundError(message)


def find_pdftoppm() -> Path | None:
    """Return Poppler's rasterizer when available."""
    discovered = shutil.which("pdftoppm")
    if discovered:
        return Path(discovered).resolve()
    codex_bundled = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "native"
        / "poppler"
        / "Library"
        / "bin"
        / "pdftoppm.exe"
    )
    return codex_bundled.resolve() if codex_bundled.is_file() else None
