import json
from pathlib import Path

import pytest

from scripts.mermaid_check.cli import main
from scripts.mermaid_check.extraction import Diagram, read_diagrams
from scripts.mermaid_check.rendering import CheckError, file_error, find_browser, pinned_bundle

MARKDOWN = """# Title

```text
graph TD
  NotADiagram
```

```mermaid
graph TD
  A --> B
```

- Item

  ```mermaid
  sequenceDiagram
    Alice->>Bob: Hi
  ```
"""


def write(path: Path, text: str) -> Path:
    path.write_bytes(text.encode())
    return path


def browser_available() -> bool:
    try:
        find_browser()
    except CheckError:
        return False
    return True


needs_browser = pytest.mark.skipif(not browser_available(), reason="No Chromium browser")


def test_markdown_diagrams_and_first_lines(tmp_path: Path) -> None:
    diagrams = read_diagrams(write(tmp_path / "doc.md", MARKDOWN))
    assert [(d.index, d.first_line) for d in diagrams] == [(1, 9), (2, 16)]
    assert diagrams[0].source == "graph TD\n  A --> B\n"
    assert diagrams[1].source.startswith("sequenceDiagram\n")


def test_mermaid_file_is_one_diagram(tmp_path: Path) -> None:
    diagrams = read_diagrams(write(tmp_path / "flow.mmd", "graph LR\n  A --> B\n"))
    assert [(d.index, d.first_line) for d in diagrams] == [(1, 1)]


def test_unsupported_file_type_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="expected"):
        read_diagrams(write(tmp_path / "notes.txt", "graph TD\n"))


def test_error_line_is_translated_to_file_line() -> None:
    diagram = Diagram(Path("doc.md"), 1, 9, "graph TD\n  A --> B\n  B -->> C\n")
    assert file_error("Parse error on line 3:", diagram).startswith("File line 11: ")
    # End-of-input errors name a line past the diagram; report its last line instead.
    assert file_error("Parse error on line 5:", diagram).startswith("File line 11: ")
    assert file_error("Unknown diagram type", diagram) == "Unknown diagram type"


def test_pinned_bundle_matches_recorded_hash() -> None:
    bundle, version = pinned_bundle()
    assert bundle.name == "mermaid.min.js"
    assert version


def test_no_diagrams_cannot_be_checked(tmp_path: Path) -> None:
    source = write(tmp_path / "plain.md", "No diagrams.\n")
    assert main([str(source), "--out-dir", str(tmp_path / "png")]) == 2


@needs_browser
def test_valid_and_invalid_diagrams_are_reported_separately(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = write(
        tmp_path / "doc.md",
        "```mermaid\ngraph TD\n  A --> B\n```\n\n```mermaid\ngraph TD\n  A -->\n```\n",
    )
    assert main([str(source), "--out-dir", str(tmp_path / "png")]) == 1
    report = json.loads(capsys.readouterr().out)
    first, second = report["diagrams"]
    assert first["status"] == "rendered"
    assert Path(first["png"]).stat().st_size > 1000
    assert second["status"] == "failed"
    assert second["error"].startswith("File line 8: ")


@needs_browser
def test_all_rendered_exits_zero(tmp_path: Path) -> None:
    source = write(tmp_path / "flow.mmd", "graph LR\n  A[\"Parse (strict)\"] --> B\n")
    assert main([str(source), "--out-dir", str(tmp_path / "png"), "--theme", "neutral"]) == 0
