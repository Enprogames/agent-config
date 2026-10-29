"""Command-line interface for Markdown structural and rendered QA."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts.markdown_qa.errors import MarkdownQaError
from scripts.markdown_qa.parsing import Issue, analyze_markdown
from scripts.markdown_qa.rendering import render_markdown_preview
from scripts.markdown_qa.verification import build_manifest, write_manifest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="markdown-qa",
        description=(
            "Validate Markdown structure and optionally render browser previews."
        ),
    )
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--input", type=Path, required=True)
    validate.add_argument("--manifest", type=Path)
    validate.add_argument("--render", action="store_true")
    validate.add_argument("--qa-dir", type=Path)
    validate.add_argument("--allow-remote-assets", action="store_true")
    return parser


def _emit(value: dict[str, object]) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def _run(arguments: argparse.Namespace) -> tuple[int, dict[str, object]]:
    if arguments.command != "validate":
        raise AssertionError(f"Unhandled command: {arguments.command}")
    if arguments.render and arguments.qa_dir is None:
        raise MarkdownQaError("--qa-dir is required when --render is used.")
    analysis = analyze_markdown(arguments.input)
    renderer = None
    if arguments.render and not analysis.errors:
        try:
            renderer = render_markdown_preview(
                analysis.path,
                arguments.qa_dir,
                allow_remote_assets=arguments.allow_remote_assets,
            )
        except MarkdownQaError as exc:
            analysis.issues.append(
                Issue("error", "render-failed", str(exc))
            )
    manifest = build_manifest(analysis, renderer)
    if arguments.manifest:
        write_manifest(manifest, arguments.manifest)
        manifest["manifest_path"] = str(arguments.manifest.resolve())
    return (2 if analysis.errors else 0), manifest


def main(argv: list[str] | None = None) -> int:
    """Run Markdown QA and emit a JSON manifest to stdout."""
    try:
        code, manifest = _run(_parser().parse_args(argv))
    except (MarkdownQaError, FileNotFoundError, UnicodeDecodeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    else:
        _emit(manifest)
        return code
