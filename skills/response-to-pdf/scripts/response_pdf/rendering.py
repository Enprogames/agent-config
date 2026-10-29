"""Render immutable Markdown to PDF through local HTML and Microsoft Edge."""

from __future__ import annotations

import html
import mimetypes
import shutil
import tempfile
import threading
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from markdown_it import MarkdownIt
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

from scripts.response_pdf.errors import RenderError
from scripts.response_pdf.paths import ASSETS_DIR, find_edge

MAX_REMOTE_IMAGE_BYTES = 25 * 1024 * 1024


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
    directory = Path(tempfile.mkdtemp(prefix="response-pdf-"))
    try:
        yield directory
    finally:
        shutil.rmtree(directory, ignore_errors=True)


class AssetResolver:
    """Copy or download image assets into an isolated render directory."""

    def __init__(self, source_dir: Path, staging_dir: Path) -> None:
        self.source_dir = source_dir
        self.media_dir = staging_dir / "media"
        self.media_dir.mkdir(parents=True, exist_ok=True)
        self._counter = 0

    def _destination(self, suffix: str) -> Path:
        self._counter += 1
        safe_suffix = suffix.lower() if suffix else ".img"
        return self.media_dir / f"asset-{self._counter:03d}{safe_suffix}"

    def resolve(self, source: str) -> str:
        if source.startswith("data:"):
            return source
        parsed = urlparse(source)
        if parsed.scheme in {"http", "https"}:
            return self._download(source)
        if parsed.scheme == "file":
            candidate = Path(unquote(parsed.path.lstrip("/")))
        else:
            candidate = Path(unquote(source))
            if not candidate.is_absolute():
                candidate = self.source_dir / candidate
        if not candidate.is_file():
            raise RenderError(f"Referenced image does not exist: {source}")
        destination = self._destination(candidate.suffix)
        shutil.copy2(candidate, destination)
        return destination.relative_to(self.media_dir.parent).as_posix()

    def _download(self, source: str) -> str:
        request = urllib.request.Request(
            source, headers={"User-Agent": "response-to-pdf/0.1"}
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                content_type = response.headers.get_content_type()
                data = response.read(MAX_REMOTE_IMAGE_BYTES + 1)
        except OSError as exc:
            raise RenderError(f"Could not download image {source}: {exc}") from exc
        if len(data) > MAX_REMOTE_IMAGE_BYTES:
            raise RenderError(f"Remote image exceeds 25 MiB: {source}")
        if not content_type.startswith("image/"):
            raise RenderError(
                f"Remote asset is not an image ({content_type}): {source}"
            )
        suffix = (
            mimetypes.guess_extension(content_type)
            or Path(urlparse(source).path).suffix
        )
        destination = self._destination(suffix)
        destination.write_bytes(data)
        return destination.relative_to(self.media_dir.parent).as_posix()


def _markdown_html(
    markdown: str, source_dir: Path, staging_dir: Path
) -> tuple[str, int]:
    resolver = AssetResolver(source_dir, staging_dir)
    parser = MarkdownIt(
        "commonmark", {"html": False, "linkify": False, "typographer": False}
    )
    parser.enable("table")
    parser.enable("strikethrough")
    default_image = parser.renderer.image
    diagram_count = 0

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
            return f'<div class="mermaid">{html.escape(token.content)}</div>\n'
        try:
            lexer = get_lexer_by_name(language) if language else TextLexer()
        except ClassNotFound:
            lexer = TextLexer()
        formatter = HtmlFormatter(cssclass="highlight", nowrap=False)
        return highlight(token.content, lexer, formatter)

    parser.renderer.rules["image"] = image_rule
    parser.renderer.rules["fence"] = fence_rule
    return parser.render(markdown), diagram_count


def _document_html(body: str, paper: str, diagram_count: int) -> str:
    css = (ASSETS_DIR / "print.css").read_text(encoding="utf-8")
    pygments_css = HtmlFormatter(cssclass="highlight").get_style_defs(".highlight")
    mermaid = ""
    if diagram_count:
        mermaid = """
<script src="vendor/mermaid.min.js"></script>
<script>
mermaid.initialize({startOnLoad: false, securityLevel: "strict", theme: "neutral"});
window.addEventListener("load", async () => {
  try {
    const diagrams = Array.from(document.querySelectorAll(".mermaid"));
    const sources = diagrams.map(diagram => diagram.textContent || "");
    for (const source of sources) {
      await mermaid.parse(source);
    }
    diagrams.forEach((diagram, index) => { diagram.textContent = sources[index]; });
    await mermaid.run({nodes: diagrams});
    await document.fonts.ready;
    await new Promise(resolve => requestAnimationFrame(
      () => requestAnimationFrame(resolve)
    ));
    document.body.dataset.renderStatus = "complete";
  } catch (error) {
    document.body.dataset.renderStatus = "error";
    document.body.dataset.renderError = String(error);
  }
});
</script>"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>@page {{ size: {paper}; }}\n{css}\n{pygments_css}</style>
</head>
<body data-render-status="{"pending" if diagram_count else "complete"}">
<main>{body}</main>
{mermaid}
</body>
</html>
"""


def _render_with_playwright(
    edge: Path,
    url: str,
    output: Path,
    diagram_count: int,
) -> str:
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=str(edge),
                headless=True,
                args=[
                    "--disable-background-networking",
                    "--disable-component-update",
                    "--disable-extensions",
                    "--disable-sync",
                ],
            )
            try:
                page = browser.new_page()
                page.goto(url, wait_until="networkidle", timeout=30_000)
                if diagram_count:
                    page.wait_for_function(
                        "document.body.dataset.renderStatus !== 'pending'",
                        timeout=20_000,
                    )
                    status = page.locator("body").get_attribute("data-render-status")
                    if status != "complete":
                        detail = page.locator("body").get_attribute("data-render-error")
                        if detail and len(detail) > 1000:
                            detail = f"{detail[:400]} ... {detail[-600:]}"
                        raise RenderError(f"Mermaid rendering failed: {detail}")
                    rendered_diagrams = page.locator(".mermaid svg").count()
                    if rendered_diagrams != diagram_count:
                        raise RenderError(
                            "Mermaid SVG count does not match the source diagram count."
                        )
                page.emulate_media(media="print")
                output.unlink(missing_ok=True)
                page.pdf(
                    path=str(output),
                    print_background=True,
                    prefer_css_page_size=True,
                )
                return browser.version
            finally:
                browser.close()
    except PlaywrightError as exc:
        raise RenderError(f"Browser rendering failed: {exc}") from exc


def render_markdown_to_pdf(
    source: Path, output: Path, paper: str = "letter"
) -> dict[str, Any]:
    """Render source Markdown to a PDF without rewriting source content."""
    source = source.resolve()
    output = output.resolve()
    if not source.is_file():
        raise RenderError(f"Markdown source does not exist: {source}")
    markdown = source.read_bytes().decode("utf-8")
    paper = paper.casefold()
    if paper not in {"letter", "a4"}:
        raise RenderError("Paper must be 'letter' or 'a4'.")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)

    edge = find_edge()
    with _staging_directory() as staging_dir:
        vendor_dir = staging_dir / "vendor"
        vendor_dir.mkdir()
        body, diagram_count = _markdown_html(markdown, source.parent, staging_dir)
        if diagram_count:
            mermaid_source = ASSETS_DIR / "vendor" / "mermaid.min.js"
            if not mermaid_source.is_file():
                raise RenderError("Pinned Mermaid asset is missing from the skill.")
            shutil.copy2(mermaid_source, vendor_dir / "mermaid.min.js")
        document = staging_dir / "document.html"
        document.write_text(
            _document_html(body, paper, diagram_count),
            encoding="utf-8",
            newline="\n",
        )
        with _serve(staging_dir) as base_url:
            browser_version = _render_with_playwright(
                edge,
                f"{base_url}/{document.name}",
                output,
                diagram_count,
            )
        if not output.is_file() or output.stat().st_size < 1000:
            raise RenderError("Microsoft Edge did not create a valid PDF.")
    return {
        "browser": str(edge),
        "browser_version": browser_version,
        "diagram_count": diagram_count,
        "engine": "playwright",
        "paper": paper,
    }
