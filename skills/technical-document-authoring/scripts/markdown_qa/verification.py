"""Build durable Markdown QA manifests."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from scripts.markdown_qa.parsing import Analysis


def sha256_file(path: Path) -> str:
    """Hash a file in bounded chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    analysis: Analysis,
    renderer: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return a serializable record of completed checks and unresolved warnings."""
    render_failed = any(issue.code == "render-failed" for issue in analysis.errors)
    structural_errors = [
        issue for issue in analysis.errors if issue.code != "render-failed"
    ]
    if renderer:
        render_status = "passed"
        visual_status = "required"
    elif render_failed:
        render_status = "failed"
        visual_status = "unavailable_due_to_render_failure"
    else:
        render_status = "not_requested"
        visual_status = "not_requested"
    return {
        "format_version": 1,
        "created_at": datetime.now(UTC).isoformat(),
        "source_path": str(analysis.path),
        "source_sha256": sha256_file(analysis.path),
        "source_bytes": analysis.path.stat().st_size,
        "status": "failed" if analysis.errors else "passed",
        "errors": [issue.as_dict() for issue in analysis.errors],
        "warnings": [issue.as_dict() for issue in analysis.warnings],
        "metrics": analysis.metrics(),
        "checks": {
            "utf8": "passed",
            "markdown_structure": "passed" if not structural_errors else "failed",
            "local_targets": "checked",
            "browser_render": render_status,
            "external_url_reachability": "not_checked",
            "code_compilation": "not_checked",
            "factual_accuracy": "requires_author_review",
        },
        "renderer": renderer,
        "visual_inspection": visual_status,
    }


def write_manifest(manifest: dict[str, Any], path: Path) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
