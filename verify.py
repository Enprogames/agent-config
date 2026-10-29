"""Check repository text files without changing them."""

import os
from pathlib import Path
import sys


MAX_DOCUMENT_LINES = 300
TEXT_EXTENSIONS = {".md", ".py", ".ps1", ".sh", ".yaml", ".yml", ".json", ".toml", ".txt"}
TEXT_FILENAMES = {".gitattributes", ".gitignore", ".editorconfig"}
IGNORED_DIRECTORIES = {".git", ".venv", ".pytest_cache", ".ruff_cache", "__pycache__"}


def verify_repository(repo):
    """Return file-specific errors for the supported repository text formats."""
    errors = []
    for folder, directories, filenames in os.walk(repo):
        directories[:] = sorted(name for name in directories if name not in IGNORED_DIRECTORIES)
        for filename in sorted(filenames):
            path = Path(folder) / filename
            if path.suffix.lower() not in TEXT_EXTENSIONS and filename not in TEXT_FILENAMES:
                continue
            relative = path.relative_to(repo).as_posix()
            data = path.read_bytes()
            try:
                content = data.decode("utf-8")
            except UnicodeDecodeError:
                errors.append(f"{relative}: must use UTF-8 encoding.")
                continue
            if content.startswith("\ufeff"):
                errors.append(f"{relative}: remove the UTF-8 byte-order mark (BOM).")
            if b"\r" in data:
                errors.append(f"{relative}: use LF line endings; found CR or CRLF.")
            if data and not data.endswith(b"\n"):
                errors.append(f"{relative}: add a final newline.")
            if path.suffix.lower() == ".md":
                lines = len(content.splitlines())
                if lines > MAX_DOCUMENT_LINES:
                    errors.append(f"{relative}: {lines} lines; maximum is {MAX_DOCUMENT_LINES}.")
    return errors


def main():
    repo = Path(__file__).resolve().parent
    try:
        errors = verify_repository(repo)
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Repository verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
