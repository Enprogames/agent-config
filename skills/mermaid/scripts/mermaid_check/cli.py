"""Command-line entry point for checking Mermaid diagrams."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts.mermaid_check.extraction import read_diagrams
from scripts.mermaid_check.rendering import CheckError, check_diagrams

THEMES = ["default", "neutral", "dark", "forest", "base"]


def main(argv: list[str] | None = None) -> int:
    """Check diagrams; exit 0 when all render, 1 when any fail, 2 when the check fails."""
    parser = argparse.ArgumentParser(
        prog="mermaid_check",
        description="Render Mermaid diagrams to PNG files and report failures.",
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="Markdown or Mermaid files")
    parser.add_argument("--out-dir", type=Path, required=True, help="PNG directory")
    parser.add_argument("--theme", choices=THEMES, default="default")
    arguments = parser.parse_args(argv)
    try:
        diagrams = [
            diagram
            for path in arguments.inputs
            for diagram in read_diagrams(path.resolve())
        ]
        if not diagrams:
            raise CheckError("No Mermaid diagrams were found in the input files.")
        report = check_diagrams(diagrams, arguments.out_dir.resolve(), arguments.theme)
    except (CheckError, OSError, UnicodeDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if all(item["status"] == "rendered" for item in report["diagrams"]) else 1
