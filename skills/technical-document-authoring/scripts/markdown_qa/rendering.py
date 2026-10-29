"""Render Markdown through a local browser and produce inspectable preview images."""

from __future__ import annotations

import html
import os
import shutil
import tempfile
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

from scripts.markdown_qa.assets import AssetResolver
from scripts.markdown_qa.errors import MarkdownQaError
from scripts.markdown_qa.parsing import GithubSlugger, inline_text

SKILL_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = SKILL_ROOT / "assets"

# The mermaid skill, installed beside this one, owns the pinned Mermaid bundle.
MERMAID_BUNDLE = SKILL_ROOT.parent / "mermaid" / "assets" / "mermaid.min.js"
VIEWPORT_WIDTH = 1440
VIEWPORT_HEIGHT = 1000
SCREENSHOT_SLICE_HEIGHT = 1200


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return


@contextmanager
def _serve(directory: Path) -> Iterator[str]:
    handler = partial(_QuietHandler, directory=str(directory))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@contextmanager
def _staging_directory() -> Iterator[Path]:
    directory = Path(tempfile.mkdtemp(prefix="markdown-qa-"))
    try:
        yield directory
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def _find_browser() -> Path:
    configured = os.environ.get("MARKDOWN_QA_BROWSER")
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
    raise MarkdownQaError(
        "No supported Chromium browser was found. Install Microsoft Edge or set "
        "MARKDOWN_QA_BROWSER to its executable."
    )


def _markdown_html(
    markdown: str,
    source_dir: Path,
    staging_dir: Path,
    *,
    allow_remote_assets: bool,
) -> tuple[str, int, AssetResolver]:
    resolver = AssetResolver(
        source_dir, staging_dir, allow_remote=allow_remote_assets
    )
    parser = MarkdownIt(
        "commonmark", {"html": False, "linkify": False, "typographer": False}
    )
    parser.enable("table")
    parser.enable("strikethrough")
    default_image = parser.renderer.image
    slugger = GithubSlugger()
    diagram_count = 0

    def heading_rule(
        tokens: list[Any], index: int, options: dict[str, Any], env: dict[str, Any]
    ) -> str:
        next_token = tokens[index + 1] if index + 1 < len(tokens) else None
        title = inline_text(next_token) if next_token is not None else ""
        tokens[index].attrSet("id", slugger.slug(title))
        return parser.renderer.renderToken(tokens, index, options, env)

    def image_rule(
        tokens: list[Any], index: int, options: dict[str, Any], env: dict[str, Any]
    ) -> str:
        token = tokens[index]
        source = token.attrGet("src")
        if source:
            token.attrSet("src", resolver.resolve(source))
        return default_image(tokens, index, options, env)

    def fence_rule(
        tokens: list[Any], index: int, _options: dict[str, Any], _env: dict[str, Any]
    ) -> str:
        nonlocal diagram_count
        token = tokens[index]
        language = token.info.strip().split(maxsplit=1)[0] if token.info.strip() else ""
        if language.casefold() == "mermaid":
            diagram_count += 1
            source = html.escape(token.content)
            return (
                f'<figure class="diagram"><div class="mermaid">{source}'
                "</div></figure>\n"
            )
        try:
            lexer = get_lexer_by_name(language) if language else TextLexer()
        except ClassNotFound:
            lexer = TextLexer()
        return highlight(
            token.content,
            lexer,
            HtmlFormatter(cssclass="highlight", nowrap=False),
        )

    parser.renderer.rules["heading_open"] = heading_rule
    parser.renderer.rules["image"] = image_rule
    parser.renderer.rules["fence"] = fence_rule
    return parser.render(markdown), diagram_count, resolver


def _document_html(body: str, diagram_count: int) -> str:
    css = (ASSETS_DIR / "preview.css").read_text(encoding="utf-8")
    pygments_css = HtmlFormatter(cssclass="highlight").get_style_defs(".highlight")
    mermaid_script = ""
    if diagram_count:
        mermaid_script = '<script src="vendor/mermaid.min.js"></script>'
    mermaid_initialization = ""
    if diagram_count:
        mermaid_initialization = """
mermaid.initialize({
  startOnLoad: false,
  securityLevel: "strict",
  theme: "neutral"
});"""
    initialization = f"""
<script>
{mermaid_initialization}
window.addEventListener("load", async () => {{
  try {{
    const diagrams = Array.from(document.querySelectorAll(".mermaid"));
    if (diagrams.length !== {diagram_count}) {{
      throw new Error("Mermaid source count changed during rendering");
    }}
    if (diagrams.length) {{
      const sources = diagrams.map(diagram => diagram.textContent || "");
      for (const source of sources) {{ await mermaid.parse(source); }}
      diagrams.forEach((diagram, index) => {{ diagram.textContent = sources[index]; }});
      await mermaid.run({{nodes: diagrams}});
    }}
    const images = Array.from(document.images);
    await Promise.all(images.map(image => new Promise((resolve, reject) => {{
      if (image.complete) {{
        image.naturalWidth > 0
          ? resolve()
          : reject(new Error(`Broken image: ${{image.src}}`));
      }} else {{
        image.addEventListener("load", resolve, {{once: true}});
        image.addEventListener(
          "error",
          () => reject(new Error(`Broken image: ${{image.src}}`)),
          {{once: true}}
        );
      }}
    }})));
    await document.fonts.ready;
    await new Promise(resolve => requestAnimationFrame(
      () => requestAnimationFrame(resolve)
    ));
    document.body.dataset.renderStatus = "complete";
  }} catch (error) {{
    document.body.dataset.renderStatus = "error";
    document.body.dataset.renderError = String(error);
  }}
}});
</script>"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{css}\n{pygments_css}</style>
</head>
<body data-render-status="pending">
<main>{body}</main>
{mermaid_script}
{initialization}
</body>
</html>
"""


def _screenshots(page: Any, qa_dir: Path) -> list[str]:
    qa_dir = qa_dir.resolve()
    qa_dir.mkdir(parents=True, exist_ok=True)
    for stale in qa_dir.glob("preview-*.png"):
        stale.unlink()
    height = int(
        page.evaluate(
            "Math.max(document.body.scrollHeight, "
            "document.documentElement.scrollHeight)"
        )
    )
    images: list[str] = []
    positions = range(0, max(height, 1), SCREENSHOT_SLICE_HEIGHT)
    for index, top in enumerate(positions, start=1):
        slice_height = min(SCREENSHOT_SLICE_HEIGHT, height - top)
        destination = qa_dir / f"preview-{index:03d}.png"
        page.screenshot(
            path=str(destination),
            clip={
                "x": 0,
                "y": top,
                "width": VIEWPORT_WIDTH,
                "height": max(slice_height, 1),
            },
        )
        images.append(str(destination))
    if not images:
        raise MarkdownQaError("Browser rendering produced no preview images.")
    return images


def _render_with_browser(
    browser_path: Path,
    url: str,
    qa_dir: Path,
    diagram_count: int,
) -> dict[str, Any]:
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
                    viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT}
                )
                page.goto(url, wait_until="networkidle", timeout=30_000)
                page.wait_for_function(
                    "document.body.dataset.renderStatus !== 'pending'", timeout=20_000
                )
                status = page.locator("body").get_attribute("data-render-status")
                if status != "complete":
                    detail = page.locator("body").get_attribute("data-render-error")
                    if detail and len(detail) > 1000:
                        detail = f"{detail[:400]} ... {detail[-600:]}"
                    raise MarkdownQaError(f"Browser rendering failed: {detail}")
                rendered_diagrams = page.locator(".mermaid svg").count()
                if rendered_diagrams != diagram_count:
                    raise MarkdownQaError(
                        "Mermaid SVG count does not match the source diagram count."
                    )
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth > "
                    "document.documentElement.clientWidth + 2"
                )
                if overflow:
                    raise MarkdownQaError(
                        "Rendered document has horizontal overflow at the QA viewport."
                    )
                images = _screenshots(page, qa_dir)
                return {
                    "browser": str(browser_path),
                    "browser_version": browser.version,
                    "engine": "playwright",
                    "viewport": {
                        "width": VIEWPORT_WIDTH,
                        "height": VIEWPORT_HEIGHT,
                    },
                    "diagram_count": diagram_count,
                    "preview_images": images,
                    "visual_inspection": "required",
                }
            finally:
                browser.close()
    except PlaywrightError as exc:
        raise MarkdownQaError(f"Browser rendering failed: {exc}") from exc


def render_markdown_preview(
    source: Path,
    qa_dir: Path,
    *,
    allow_remote_assets: bool = False,
) -> dict[str, Any]:
    """Render Markdown to browser preview images without modifying the source."""
    source = source.resolve()
    markdown = source.read_bytes().decode("utf-8")
    browser_path = _find_browser()
    with _staging_directory() as staging_dir:
        vendor_dir = staging_dir / "vendor"
        vendor_dir.mkdir()
        body, diagram_count, resolver = _markdown_html(
            markdown,
            source.parent,
            staging_dir,
            allow_remote_assets=allow_remote_assets,
        )
        if diagram_count:
            if not MERMAID_BUNDLE.is_file():
                raise MarkdownQaError(
                    f"Install the mermaid skill beside this skill: {MERMAID_BUNDLE}"
                )
            shutil.copy2(MERMAID_BUNDLE, vendor_dir / "mermaid.min.js")
        document = staging_dir / "document.html"
        document.write_text(
            _document_html(body, diagram_count),
            encoding="utf-8",
            newline="\n",
        )
        with _serve(staging_dir) as base_url:
            result = _render_with_browser(
                browser_path,
                f"{base_url}/{document.name}",
                qa_dir,
                diagram_count,
            )
        result["local_assets"] = resolver.local_count
        result["remote_assets"] = resolver.remote_count
        return result
