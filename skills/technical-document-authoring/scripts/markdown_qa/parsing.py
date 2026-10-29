"""Structural Markdown analysis, local-target checks, and issue reporting."""

from __future__ import annotations

import base64
import binascii
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from markdown_it import MarkdownIt

FENCE_PATTERN = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
HEADING_PATTERN = re.compile(r"[^\w\- ]", re.UNICODE)
WINDOWS_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:[\\/]")


@dataclass(frozen=True)
class Issue:
    """A validation error or warning tied to a source line when available."""

    severity: str
    code: str
    message: str
    line: int | None = None

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }
        if self.line is not None:
            result["line"] = self.line
        return result


@dataclass
class Analysis:
    """Parsed source and deterministic structural findings."""

    path: Path
    markdown: str
    issues: list[Issue] = field(default_factory=list)
    heading_count: int = 0
    link_count: int = 0
    external_link_count: int = 0
    image_count: int = 0
    remote_image_count: int = 0
    code_block_count: int = 0
    mermaid_count: int = 0
    table_count: int = 0

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    def metrics(self) -> dict[str, int]:
        return {
            "headings": self.heading_count,
            "links": self.link_count,
            "external_links_not_reached": self.external_link_count,
            "images": self.image_count,
            "remote_images": self.remote_image_count,
            "code_blocks": self.code_block_count,
            "mermaid_diagrams": self.mermaid_count,
            "tables": self.table_count,
        }


class GithubSlugger:
    """Create predictable GitHub-like heading anchors, including duplicate suffixes."""

    def __init__(self) -> None:
        self._seen: dict[str, int] = {}

    def slug(self, value: str) -> str:
        base = HEADING_PATTERN.sub("", value.casefold().strip())
        base = re.sub(r"\s+", "-", base)
        base = re.sub(r"-+", "-", base).strip("-") or "section"
        duplicate = self._seen.get(base, 0)
        self._seen[base] = duplicate + 1
        return base if duplicate == 0 else f"{base}-{duplicate}"


def inline_text(token: Any) -> str:
    """Return visible text from a Markdown-It inline token."""
    if not token.children:
        return token.content
    parts: list[str] = []
    for child in token.children:
        if child.type in {"text", "code_inline", "image"}:
            parts.append(child.content)
        elif child.type in {"softbreak", "hardbreak"}:
            parts.append(" ")
    return "".join(parts).strip()


def _line(token: Any) -> int | None:
    return token.map[0] + 1 if token.map else None


def _check_fences(markdown: str, issues: list[Issue]) -> None:
    opened: tuple[str, int, int] | None = None
    for number, line in enumerate(markdown.splitlines(), start=1):
        match = FENCE_PATTERN.match(line)
        if not match:
            continue
        marker = match.group(2)
        if opened is None:
            if marker[0] == "`" and "`" in match.group(3):
                continue
            opened = (marker[0], len(marker), number)
            continue
        character, minimum, _opening_line = opened
        is_closing = (
            marker[0] == character
            and len(marker) >= minimum
            and not match.group(3).strip()
        )
        if is_closing:
            opened = None
    if opened is not None:
        issues.append(
            Issue(
                "error",
                "unclosed-fence",
                "Fenced code block is not closed.",
                opened[2],
            )
        )


def _split_local_target(target: str) -> str:
    value = unquote(target)
    value = value.split("#", maxsplit=1)[0]
    value = value.split("?", maxsplit=1)[0]
    return value


def _file_uri_path(target: str) -> Path:
    parsed = urlparse(target)
    value = unquote(parsed.path)
    if re.match(r"^/[A-Za-z]:/", value):
        value = value[1:]
    return Path(value)


def _local_path(target: str, source_dir: Path) -> Path | None:
    if target.startswith("#"):
        return None
    if WINDOWS_DRIVE_PATTERN.match(target):
        return Path(_split_local_target(target))
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto", "data"}:
        return None
    if parsed.scheme == "file":
        candidate = _file_uri_path(target)
    elif parsed.scheme:
        return None
    else:
        value = _split_local_target(target)
        if not value:
            candidate = source_dir
        else:
            candidate = Path(value)
            if not candidate.is_absolute():
                candidate = source_dir / candidate
    return candidate


def _image_kind(path: Path) -> str | None:
    try:
        header = path.read_bytes()[:512]
    except OSError:
        return None
    kind = None
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        kind = "png"
    elif header.startswith(b"\xff\xd8\xff"):
        kind = "jpeg"
    elif header.startswith((b"GIF87a", b"GIF89a")):
        kind = "gif"
    elif header.startswith(b"RIFF") and header[8:12] == b"WEBP":
        kind = "webp"
    elif header.startswith(b"BM"):
        kind = "bmp"
    elif header.startswith(b"\x00\x00\x01\x00"):
        kind = "ico"
    elif path.suffix.casefold() == ".svg":
        try:
            prefix = path.read_text(encoding="utf-8", errors="ignore")[:4096]
        except OSError:
            return None
        if re.search(r"<svg(?:\s|>)", prefix, re.IGNORECASE):
            kind = "svg"
    return kind


def _validate_data_image(target: str) -> bool:
    try:
        header, payload = target.split(",", maxsplit=1)
    except ValueError:
        return False
    if not header.casefold().startswith("data:image/"):
        return False
    if ";base64" in header.casefold():
        try:
            base64.b64decode(payload, validate=True)
        except (ValueError, binascii.Error):
            return False
    return bool(payload)


def _heading_data(tokens: list[Any], issues: list[Issue]) -> set[str]:
    slugger = GithubSlugger()
    anchors: set[str] = set()
    prior_level: int | None = None
    h1_count = 0
    raw_seen: dict[str, int] = {}
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        level = int(token.tag[1])
        text = inline_text(tokens[index + 1]) if index + 1 < len(tokens) else ""
        anchor = slugger.slug(text)
        anchors.add(anchor)
        raw_seen[text.casefold()] = raw_seen.get(text.casefold(), 0) + 1
        if prior_level is not None and level > prior_level + 1:
            issues.append(
                Issue(
                    "warning",
                    "heading-level-jump",
                    f"Heading level jumps from h{prior_level} to h{level}.",
                    _line(token),
                )
            )
        prior_level = level
        if level == 1:
            h1_count += 1
    if h1_count > 1:
        issues.append(
            Issue(
                "warning",
                "multiple-h1",
                f"Document contains {h1_count} level-one headings.",
            )
        )
    duplicates = [text for text, count in raw_seen.items() if text and count > 1]
    if duplicates:
        issues.append(
            Issue(
                "warning",
                "duplicate-heading",
                "Repeated heading text creates suffixed anchors: "
                + ", ".join(repr(value) for value in duplicates[:5]),
            )
        )
    return anchors


def _check_link(
    target: str,
    source: Path,
    anchors: set[str],
    issues: list[Issue],
    line: int | None,
) -> bool:
    if target.startswith("#"):
        anchor = unquote(target[1:]).casefold()
        if not anchor or anchor not in anchors:
            issues.append(
                Issue(
                    "error",
                    "missing-anchor",
                    f"Internal link target does not match a heading anchor: {target}",
                    line,
                )
            )
        return False
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto"}:
        return True
    candidate = _local_path(target, source.parent)
    if candidate is not None and not candidate.exists():
        issues.append(
            Issue(
                "error",
                "missing-local-link",
                f"Local link target does not exist: {target}",
                line,
            )
        )
    return False


def _check_image(
    target: str,
    alt: str,
    source: Path,
    issues: list[Issue],
    line: int | None,
) -> bool:
    if not alt.strip():
        issues.append(
            Issue(
                "warning",
                "missing-image-alt",
                (
                    "Image has empty alt text; confirm it is decorative or add "
                    "useful text."
                ),
                line,
            )
        )
    if target.startswith("data:"):
        if not _validate_data_image(target):
            issues.append(
                Issue("error", "invalid-data-image", "Image data URI is invalid.", line)
            )
        return False
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https"}:
        return True
    candidate = _local_path(target, source.parent)
    if candidate is None or not candidate.is_file():
        issues.append(
            Issue(
                "error",
                "missing-local-image",
                f"Referenced local image does not exist: {target}",
                line,
            )
        )
    elif _image_kind(candidate) is None:
        issues.append(
            Issue(
                "error",
                "invalid-local-image",
                f"Referenced file is not a supported image: {target}",
                line,
            )
        )
    return False


def analyze_markdown(path: Path) -> Analysis:
    """Parse and validate a UTF-8 Markdown file without network access."""
    path = path.resolve()
    markdown = path.read_bytes().decode("utf-8")
    analysis = Analysis(path=path, markdown=markdown)
    _check_fences(markdown, analysis.issues)

    parser = MarkdownIt(
        "commonmark", {"html": False, "linkify": False, "typographer": False}
    )
    parser.enable("table")
    parser.enable("strikethrough")
    tokens = parser.parse(markdown)
    anchors = _heading_data(tokens, analysis.issues)
    analysis.heading_count = sum(token.type == "heading_open" for token in tokens)
    analysis.table_count = sum(token.type == "table_open" for token in tokens)

    for token in tokens:
        if token.type in {"fence", "code_block"}:
            analysis.code_block_count += 1
            language = token.info.strip().split(maxsplit=1)[0] if token.info else ""
            if token.type == "fence" and language.casefold() == "mermaid":
                analysis.mermaid_count += 1
                if not token.content.strip():
                    analysis.issues.append(
                        Issue(
                            "error",
                            "empty-mermaid",
                            "Mermaid block is empty.",
                            _line(token),
                        )
                    )
            elif token.content.strip() and not language:
                analysis.issues.append(
                    Issue(
                        "warning",
                        "missing-code-language",
                        (
                            "Fenced code block has no language identifier; use 'text' "
                            "when intentional."
                        ),
                        _line(token),
                    )
                )
        if token.type != "inline" or not token.children:
            continue
        source_line = _line(token)
        for child in token.children:
            if child.type == "link_open":
                target = child.attrGet("href") or ""
                analysis.link_count += 1
                if _check_link(
                    target, analysis.path, anchors, analysis.issues, source_line
                ):
                    analysis.external_link_count += 1
            elif child.type == "image":
                target = child.attrGet("src") or ""
                analysis.image_count += 1
                if _check_image(
                    target,
                    child.content,
                    analysis.path,
                    analysis.issues,
                    source_line,
                ):
                    analysis.remote_image_count += 1
    return analysis
