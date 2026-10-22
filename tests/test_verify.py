from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from verify import verify_repository


class VerifyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)

    def test_repository_passes_verification(self):
        self.assertEqual(verify_repository(Path(__file__).resolve().parents[1]), [])

    def test_accepts_unicode_empty_files_and_supported_text_formats(self):
        for name in ("README.md", "script.py", "setup.ps1", "setup.sh", "config.yaml",
                     "config.yml", "config.json", "config.toml", "notes.txt",
                     ".gitattributes", ".gitignore", ".editorconfig"):
            (self.repo / name).write_bytes("Text with caf\u00e9\n".encode("utf-8"))
        (self.repo / "empty.txt").write_bytes(b"")
        self.assertEqual(verify_repository(self.repo), [])

    def test_reports_invalid_formats_without_changing_files(self):
        cases = [
            (b"\xef\xbb\xbfText\n", "BOM"),
            (b"\xff\n", "UTF-8 encoding"),
            (b"Text\r\n", "LF line endings"),
            (b"First\rSecond\n", "LF line endings"),
            (b"Text", "final newline"),
            (b"Line\n" * 301, "301 lines; maximum is 300"),
        ]
        document = self.repo / "invalid.MD"
        for content, expected in cases:
            with self.subTest(problem=expected, content=content[:20]):
                document.write_bytes(content)
                errors = verify_repository(self.repo)
                self.assertTrue(any("invalid.MD:" in error and expected in error for error in errors))
                self.assertEqual(document.read_bytes(), content)

    def test_reports_multiple_files_and_problems(self):
        (self.repo / "first.md").write_bytes(b"\xef\xbb\xbfFirst\r\n")
        (self.repo / "second.txt").write_bytes(b"Second")
        errors = verify_repository(self.repo)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any("first.md:" in error and "BOM" in error for error in errors))
        self.assertTrue(any("first.md:" in error and "LF line endings" in error for error in errors))
        self.assertTrue(any("second.txt:" in error and "final newline" in error for error in errors))

    def test_ignores_generated_directories_and_binary_assets(self):
        for folder in (".git", ".venv", "__pycache__"):
            directory = self.repo / folder
            directory.mkdir()
            (directory / "ignored.md").write_bytes(b"\xff")
        assets = self.repo / "assets"
        assets.mkdir()
        (assets / "image.png").write_bytes(b"\x89PNG\x00\xff")
        self.assertEqual(verify_repository(self.repo), [])

    def test_cli_exit_codes_and_read_only_behavior(self):
        script = self.repo / "verify.py"
        source = Path(__file__).resolve().parents[1] / "verify.py"
        script.write_bytes(source.read_bytes())
        success = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertIn("verification passed", success.stdout)

        invalid = self.repo / "invalid.md"
        invalid.write_bytes(b"No final newline")
        failure = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(failure.returncode, 1)
        self.assertIn("invalid.md: add a final newline", failure.stderr)
        self.assertEqual(invalid.read_bytes(), b"No final newline")


if __name__ == "__main__":
    unittest.main()
