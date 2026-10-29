"""Command-line interface for response capture, rendering, and printing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from scripts.response_pdf.codex_capture import capture_last_codex_answer
from scripts.response_pdf.errors import ResponsePdfError
from scripts.response_pdf.printing import (
    execute_print,
    list_printers,
    prepare_print,
)
from scripts.response_pdf.rendering import render_markdown_to_pdf
from scripts.response_pdf.verification import (
    load_verified_manifest,
    verify_pdf,
    write_manifest,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="response-to-pdf",
        description="Verbatim Markdown-to-PDF and approval-gated printing.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    capture = commands.add_parser("capture-codex")
    capture.add_argument("--output", type=Path, required=True)

    render = commands.add_parser("render")
    render.add_argument("--input", type=Path, required=True)
    render.add_argument("--output", type=Path, required=True)
    render.add_argument("--paper", choices=["letter", "a4"], default="letter")
    render.add_argument("--qa-dir", type=Path)
    render.add_argument("--manifest", type=Path)

    verify = commands.add_parser("verify")
    verify.add_argument("--manifest", type=Path, required=True)

    commands.add_parser("printers")

    plan = commands.add_parser("prepare-print")
    plan.add_argument("--manifest", type=Path, required=True)
    plan.add_argument("--plan", type=Path)
    plan.add_argument("--printer")
    plan.add_argument("--settings")

    submit = commands.add_parser("print")
    submit.add_argument("--plan", type=Path, required=True)
    submit.add_argument("--approval-code", required=True)
    submit.add_argument("--validate-only", action="store_true")
    return parser


def _emit(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def _run(arguments: argparse.Namespace) -> dict[str, Any] | list[dict[str, Any]]:
    if arguments.command == "capture-codex":
        return capture_last_codex_answer(arguments.output)
    if arguments.command == "render":
        manifest_path = arguments.manifest or arguments.output.with_suffix(
            arguments.output.suffix + ".manifest.json"
        )
        manifest_path.unlink(missing_ok=True)
        renderer = render_markdown_to_pdf(
            arguments.input, arguments.output, arguments.paper
        )
        manifest = verify_pdf(
            arguments.input,
            arguments.output,
            renderer=renderer,
            qa_dir=arguments.qa_dir,
        )
        write_manifest(manifest, manifest_path)
        manifest["manifest_path"] = str(manifest_path.resolve())
        return manifest
    if arguments.command == "verify":
        return load_verified_manifest(arguments.manifest)
    if arguments.command == "printers":
        return list_printers()
    if arguments.command == "prepare-print":
        plan_path = arguments.plan or arguments.manifest.with_suffix(".print-plan.json")
        return prepare_print(
            arguments.manifest, plan_path, arguments.printer, arguments.settings
        )
    if arguments.command == "print":
        return execute_print(
            arguments.plan,
            arguments.approval_code,
            validate_only=arguments.validate_only,
        )
    raise AssertionError(f"Unhandled command: {arguments.command}")


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    try:
        _emit(_run(_parser().parse_args(argv)))
    except (ResponsePdfError, FileNotFoundError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
