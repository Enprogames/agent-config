"""Fail when maintained text files exceed the project line limit."""

from __future__ import annotations

import sys
from pathlib import Path

MAX_LINES = 600
ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = {".py", ".md", ".toml", ".css", ".yaml", ".json"}


def main() -> int:
    """Check maintained source files and print any violations."""
    violations: list[tuple[Path, int]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in SUFFIXES:
            continue
        if any(part in {".venv", "vendor", "tools"} for part in path.parts):
            continue
        count = len(path.read_text(encoding="utf-8").splitlines())
        if count > MAX_LINES:
            violations.append((path.relative_to(ROOT), count))
    for path, count in violations:
        print(f"{path}: {count} lines (maximum {MAX_LINES})")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
