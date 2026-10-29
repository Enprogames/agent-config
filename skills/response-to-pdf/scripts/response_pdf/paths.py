"""Stable skill paths and executable discovery."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = SKILL_ROOT / "assets"
SETTINGS_PATH = SKILL_ROOT / "settings.json"
SUMATRA_PATH = SKILL_ROOT / "tools" / "SumatraPDF.exe"
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
