"""Render diagrams with the pinned Mermaid bundle in a local Chromium browser."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from scripts.mermaid_check.extraction import Diagram

SKILL_ROOT = Path(__file__).resolve().parents[2]
VERSIONS_PATH = SKILL_ROOT / "assets" / "versions.json"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
body { margin: 0; background: white; }
.diagram { display: inline-block; padding: 16px; background: white; }
</style>
</head>
<body></body>
</html>
"""

# Renders each diagram separately so one failure does not hide the others.
RENDER_SCRIPT = """
async ({sources, theme}) => {
  mermaid.initialize({startOnLoad: false, securityLevel: "strict", theme});
  const results = [];
  for (const [index, source] of sources.entries()) {
    const container = document.createElement("div");
    container.className = "diagram";
    container.id = `diagram-${index}`;
    document.body.appendChild(container);
    try {
      await mermaid.parse(source);
      const {svg} = await mermaid.render(`svg-${index}`, source);
      container.innerHTML = svg;
      const box = container.querySelector("svg").getBoundingClientRect();
      results.push(box.width > 0 && box.height > 0
        ? {ok: true}
        : {ok: false, error: "Rendered SVG is empty."});
    } catch (error) {
      // Mermaid can leave its temporary render element behind after a failure.
      document.getElementById(`dsvg-${index}`)?.remove();
      container.remove();
      results.push({ok: false, error: String(error?.message ?? error)});
    }
  }
  await document.fonts.ready;
  return results;
}
"""


class CheckError(Exception):
    """The check could not run."""


def pinned_bundle() -> tuple[Path, str]:
    """Return the Mermaid bundle and its version after checking its recorded hash."""
    entry = json.loads(VERSIONS_PATH.read_text(encoding="utf-8"))["mermaid"]
    bundle = SKILL_ROOT / entry["file"]
    if not bundle.is_file():
        raise CheckError(f"Pinned Mermaid bundle is missing: {bundle}")
    digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
    if digest != entry["sha256"].casefold():
        raise CheckError(f"Mermaid bundle does not match {VERSIONS_PATH.name}: {bundle}")
    return bundle, entry["version"]


def find_browser() -> Path:
    """Return a Chromium-based browser executable."""
    configured = os.environ.get("MERMAID_CHECK_BROWSER")
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
    raise CheckError(
        "No supported Chromium browser was found. Install Microsoft Edge or set "
        "MERMAID_CHECK_BROWSER to its executable."
    )


def file_error(error: str, diagram: Diagram) -> str:
    """Prefix a Mermaid error with the input file line it refers to."""
    match = re.search(r"line (\d+)", error)
    if not match:
        return error
    # Errors at the end of input name a line after the diagram's last line.
    line = min(int(match.group(1)), max(len(diagram.source.splitlines()), 1))
    return f"File line {diagram.first_line + line - 1}: {error}"


def check_diagrams(
    diagrams: list[Diagram], out_dir: Path, theme: str
) -> dict[str, Any]:
    """Render every diagram, save a PNG for each success, and describe each result."""
    bundle, version = pinned_bundle()
    browser_path = find_browser()
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=str(browser_path),
                headless=True,
                args=[
                    "--disable-background-networking",
                    "--disable-component-update",
                    "--disable-extensions",
                    "--disable-sync",
                ],
            )
            try:
                page = browser.new_page(
                    viewport={"width": 1600, "height": 1000}, device_scale_factor=2
                )
                page.set_content(PAGE)
                page.add_script_tag(path=str(bundle))
                outcomes = page.evaluate(
                    RENDER_SCRIPT,
                    {"sources": [diagram.source for diagram in diagrams], "theme": theme},
                )
                for number, (diagram, outcome) in enumerate(
                    zip(diagrams, outcomes, strict=True)
                ):
                    result: dict[str, Any] = {
                        "file": str(diagram.path),
                        "diagram": diagram.index,
                        "line": diagram.first_line,
                    }
                    if outcome["ok"]:
                        png = out_dir / (
                            f"{number + 1:03d}-{diagram.path.stem}-{diagram.index}.png"
                        )
                        page.locator(f"#diagram-{number}").screenshot(path=str(png))
                        result.update(status="rendered", png=str(png))
                    else:
                        error = file_error(outcome["error"], diagram)
                        result.update(status="failed", error=error)
                    results.append(result)
            finally:
                browser.close()
    except PlaywrightError as exc:
        raise CheckError(f"Browser rendering failed: {exc}") from exc
    return {
        "mermaid_version": version,
        "browser": str(browser_path),
        "diagrams": results,
        "visual_inspection": "required",
    }
