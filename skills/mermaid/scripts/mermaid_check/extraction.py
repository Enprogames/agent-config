"""Find Mermaid diagrams in Markdown and Mermaid source files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from markdown_it import MarkdownIt

MARKDOWN_SUFFIXES = {".md", ".markdown"}
MERMAID_SUFFIXES = {".mmd", ".mermaid"}


@dataclass(frozen=True)
class Diagram:
    path: Path
    index: int  # Position of the diagram within its file, starting at 1.
    first_line: int  # File line of the diagram's first source line, starting at 1.
    source: str


def read_diagrams(path: Path) -> list[Diagram]:
    """Return every diagram in a Markdown or Mermaid file."""
    text = path.read_bytes().decode("utf-8-sig")
    suffix = path.suffix.casefold()
    if suffix in MERMAID_SUFFIXES:
        return [Diagram(path, 1, 1, text)]
    if suffix not in MARKDOWN_SUFFIXES:
        raise ValueError(f"{path}: expected a .md, .markdown, .mmd, or .mermaid file.")
    fences = [
        token
        for token in MarkdownIt("commonmark").parse(text)
        if token.type == "fence" and token.info.split()[:1] == ["mermaid"]
    ]
    # token.map[0] is the zero-based line of the opening fence.
    return [
        Diagram(path, index, fence.map[0] + 2, fence.content)
        for index, fence in enumerate(fences, start=1)
    ]
