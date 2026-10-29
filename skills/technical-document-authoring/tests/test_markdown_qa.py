"""Behavioral tests for deterministic Markdown validation."""

from __future__ import annotations

from pathlib import Path

from scripts.markdown_qa.parsing import analyze_markdown

TINY_PNG = b"\x89PNG\r\n\x1a\n" + b"valid-enough-for-structural-check"


def _codes(path: Path, severity: str) -> set[str]:
    analysis = analyze_markdown(path)
    return {
        issue.code for issue in analysis.issues if issue.severity == severity
    }


def test_valid_document_resolves_targets_and_duplicate_anchor(
    tmp_path: Path,
) -> None:
    image = tmp_path / "diagram.png"
    image.write_bytes(TINY_PNG)
    source = tmp_path / "document.md"
    source.write_text(
        """# Guide

[Second copy](#details-1)

![A useful diagram](diagram.png)

## Details

```python
print("checked")
```

## Details

Text.
""",
        encoding="utf-8",
    )
    analysis = analyze_markdown(source)
    assert not analysis.errors
    assert "duplicate-heading" in {issue.code for issue in analysis.warnings}
    assert analysis.image_count == 1
    assert analysis.code_block_count == 1


def test_missing_local_targets_fail(tmp_path: Path) -> None:
    source = tmp_path / "document.md"
    source.write_text(
        "# Guide\n\n[Missing](missing.md)\n\n![Image](missing.png)\n",
        encoding="utf-8",
    )
    assert _codes(source, "error") == {
        "missing-local-image",
        "missing-local-link",
    }


def test_unclosed_fence_fails(tmp_path: Path) -> None:
    source = tmp_path / "document.md"
    source.write_text("# Guide\n\n```rust\nfn main() {}\n", encoding="utf-8")
    assert "unclosed-fence" in _codes(source, "error")


def test_empty_alt_and_heading_jump_warn(tmp_path: Path) -> None:
    image = tmp_path / "diagram.png"
    image.write_bytes(TINY_PNG)
    source = tmp_path / "document.md"
    source.write_text(
        "# Guide\n\n### Detail\n\n![](diagram.png)\n",
        encoding="utf-8",
    )
    assert _codes(source, "warning") == {
        "heading-level-jump",
        "missing-image-alt",
    }


def test_missing_internal_anchor_fails(tmp_path: Path) -> None:
    source = tmp_path / "document.md"
    source.write_text("# Guide\n\n[No target](#absent)\n", encoding="utf-8")
    assert "missing-anchor" in _codes(source, "error")
