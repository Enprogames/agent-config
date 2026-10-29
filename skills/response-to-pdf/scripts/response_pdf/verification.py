"""Structural, textual, hash, and raster verification for generated PDFs."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unicodedata
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from markdown_it import MarkdownIt
from pypdf import PdfReader

from scripts.response_pdf.errors import VerificationError
from scripts.response_pdf.paths import find_pdftoppm


def sha256_file(path: Path) -> str:
    """Hash a file in bounded chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).split())


def _visible_fragments(markdown: str) -> list[tuple[str, bool]]:
    parser = MarkdownIt("commonmark", {"html": False, "linkify": False})
    parser.enable("table")
    parser.enable("strikethrough")
    fragments: list[tuple[str, bool]] = []
    for token in parser.parse(markdown):
        if token.type == "inline" and token.children:
            parts: list[str] = []
            for child in token.children:
                if child.type in {"text", "code_inline"}:
                    parts.append(child.content)
                elif child.type in {"softbreak", "hardbreak"}:
                    parts.append(" ")
            value = _normalized("".join(parts))
            if len(value) >= 3:
                fragments.append((value, False))
        elif token.type in {"fence", "code_block"}:
            language = token.info.strip().split(maxsplit=1)[0] if token.info else ""
            if language.casefold() != "mermaid":
                value = _normalized(token.content)
                if len(value) >= 3:
                    fragments.append((value, True))
    return fragments


def _assert_text_fidelity(markdown: str, extracted: str) -> int:
    normalized_pdf = _normalized(extracted)
    compact_pdf = "".join(normalized_pdf.split())
    missing = [
        fragment
        for fragment, compact in _visible_fragments(markdown)
        if (
            "".join(fragment.split()) not in compact_pdf
            if compact
            else fragment not in normalized_pdf
        )
    ]
    if missing:
        examples = "; ".join(repr(value[:100]) for value in missing[:5])
        raise VerificationError(
            f"PDF text verification lost {len(missing)} visible fragment(s): {examples}"
        )
    return len(_visible_fragments(markdown))


def _expected_external_links(markdown: str) -> list[str]:
    parser = MarkdownIt("commonmark", {"html": False, "linkify": False})
    links: list[str] = []
    for token in parser.parse(markdown):
        if token.type != "inline" or not token.children:
            continue
        for child in token.children:
            if child.type != "link_open":
                continue
            target = child.attrGet("href")
            if target and urlparse(target).scheme in {"http", "https", "mailto"}:
                links.append(target)
    return links


def _pdf_external_links(reader: PdfReader) -> list[str]:
    links: list[str] = []
    for page in reader.pages:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            action = annotation.get("/A")
            if hasattr(action, "get_object"):
                action = action.get_object()
            if not hasattr(action, "get") or str(action.get("/S")) != "/URI":
                continue
            target = action.get("/URI")
            if target:
                links.append(str(target))
    return links


def _assert_link_fidelity(markdown: str, reader: PdfReader) -> int:
    expected = Counter(_expected_external_links(markdown))
    actual = Counter(_pdf_external_links(reader))
    missing = expected - actual
    if missing:
        targets = ", ".join(repr(target) for target in list(missing)[:5])
        raise VerificationError(f"PDF lost external hyperlink target(s): {targets}")
    return sum(expected.values())


def rasterize_pdf(pdf: Path, qa_dir: Path) -> list[str]:
    """Render every page to PNG using Poppler for visual inspection."""
    executable = find_pdftoppm()
    if executable is None:
        raise VerificationError("pdftoppm is required for visual PDF verification.")
    qa_dir = qa_dir.resolve()
    qa_dir.mkdir(parents=True, exist_ok=True)
    for stale in qa_dir.glob("page-*.png"):
        stale.unlink()
    prefix = qa_dir / "page"
    command = [str(executable), "-png", "-r", "144", str(pdf), str(prefix)]
    completed = subprocess.run(
        command, check=False, capture_output=True, text=True, timeout=120
    )
    if completed.returncode:
        raise VerificationError(f"PDF rasterization failed: {completed.stderr.strip()}")
    images = sorted(qa_dir.glob("page-*.png"))
    if not images:
        raise VerificationError("PDF rasterization produced no page images.")
    return [str(path) for path in images]


def verify_pdf(
    source: Path,
    pdf: Path,
    *,
    renderer: dict[str, Any],
    qa_dir: Path | None,
) -> dict[str, Any]:
    """Verify a PDF and return a durable manifest dictionary."""
    source = source.resolve()
    pdf = pdf.resolve()
    if not source.is_file() or not pdf.is_file():
        raise VerificationError("Source Markdown and PDF must both exist.")
    source_bytes = source.read_bytes()
    markdown = source_bytes.decode("utf-8")
    try:
        reader = PdfReader(pdf)
        page_count = len(reader.pages)
        extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise VerificationError(f"Could not reopen generated PDF: {exc}") from exc
    if page_count < 1:
        raise VerificationError("Generated PDF contains no pages.")
    checked_fragments = _assert_text_fidelity(markdown, extracted)
    checked_links = _assert_link_fidelity(markdown, reader)
    qa_images = rasterize_pdf(pdf, qa_dir) if qa_dir else []
    return {
        "format_version": 1,
        "created_at": datetime.now(UTC).isoformat(),
        "source_path": str(source),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_bytes": len(source_bytes),
        "pdf_path": str(pdf),
        "pdf_sha256": sha256_file(pdf),
        "pdf_bytes": pdf.stat().st_size,
        "page_count": page_count,
        "checked_text_fragments": checked_fragments,
        "checked_external_links": checked_links,
        "qa_images": qa_images,
        "renderer": renderer,
        "verification": "passed",
    }


def write_manifest(manifest: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load_verified_manifest(path: Path) -> dict[str, Any]:
    """Load a manifest and prove its files have not changed."""
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"Invalid manifest: {exc}") from exc
    source = Path(manifest.get("source_path", ""))
    pdf = Path(manifest.get("pdf_path", ""))
    if not source.is_file() or not pdf.is_file():
        raise VerificationError("Manifest source or PDF no longer exists.")
    if sha256_file(source) != manifest.get("source_sha256"):
        raise VerificationError("Markdown source changed after PDF verification.")
    if sha256_file(pdf) != manifest.get("pdf_sha256"):
        raise VerificationError("PDF changed after verification.")
    if manifest.get("verification") != "passed":
        raise VerificationError("Manifest does not record successful verification.")
    return manifest
