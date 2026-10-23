import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from sync import sync


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.home = self.root / "home"
        self.repo.mkdir()
        self.home.mkdir()
        (self.repo / "INSTRUCTIONS.md").write_bytes(b"Shared preferences\n")
        self.skill = self.repo / "skills" / "example" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_bytes(b"Example skill\n")
        self.reference = self.repo / "references" / "design" / "examples.md"
        self.reference.parent.mkdir(parents=True)
        self.reference.write_bytes(b"Design examples\n")

    def run_sync(self, agents=None, **options):
        with contextlib.redirect_stdout(io.StringIO()):
            return sync(self.repo, self.home, agents or ["codex"], **options)

    def test_preview_does_not_create_installed_files_or_state(self):
        self.assertEqual(self.run_sync(), 3)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_collision_prevents_all_writes(self):
        instruction = self.home / ".codex" / "AGENTS.md"
        instruction.parent.mkdir()
        instruction.write_text("Existing user preference\n")
        with self.assertRaises(ValueError):
            self.run_sync(apply=True)
        self.assertEqual(instruction.read_text(), "Existing user preference\n")
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse((self.home / ".agent-config").exists())

    def test_explicit_replacement_backs_up_then_installs_idempotently(self):
        instruction = self.home / ".codex" / "AGENTS.md"
        instruction.parent.mkdir()
        instruction.write_text("Original\n")
        self.run_sync(apply=True, replace_existing=True)
        backups = list((self.home / ".agent-config" / "backups").glob("*/.codex/AGENTS.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "Original\n")
        self.assertEqual(instruction.read_bytes(), (self.repo / "INSTRUCTIONS.md").read_bytes())
        self.assertEqual(self.run_sync(), 0)

    def test_source_update_replaces_unchanged_installed_copy(self):
        self.run_sync(apply=True)
        (self.repo / "INSTRUCTIONS.md").write_bytes(b"Revised preferences\n")
        self.run_sync(apply=True)
        self.assertEqual((self.home / ".codex" / "AGENTS.md").read_text(), "Revised preferences\n")

    def test_local_edits_block_update(self):
        self.run_sync(apply=True)
        installed = self.home / ".agents" / "skills" / "example" / "SKILL.md"
        installed.write_text("Local edit\n")
        with self.assertRaises(ValueError):
            self.run_sync(apply=True)
        self.assertEqual(installed.read_text(), "Local edit\n")

    def test_removed_shared_file_preserves_unmanaged_neighbor(self):
        self.run_sync(apply=True)
        installed_folder = self.home / ".agents" / "skills" / "example"
        neighbor = installed_folder / "personal.txt"
        neighbor.write_text("Keep this\n")
        self.skill.unlink()
        self.run_sync(apply=True)
        self.assertFalse((installed_folder / "SKILL.md").exists())
        self.assertEqual(neighbor.read_text(), "Keep this\n")

    def test_selected_agents_receive_identical_bytes(self):
        self.run_sync(agents=["claude", "antigravity", "antigravity-cli"], apply=True)
        for path in (".claude/CLAUDE.md", ".gemini/GEMINI.md"):
            self.assertEqual((self.home / path).read_bytes(), (self.repo / "INSTRUCTIONS.md").read_bytes())
        for path in (".claude/skills", ".gemini/config/skills", ".gemini/antigravity-cli/skills"):
            self.assertEqual((self.home / path / "example/SKILL.md").read_bytes(), self.skill.read_bytes())
        self.assertFalse((self.home / ".codex").exists())
        self.assertEqual(self.run_sync(agents=["claude", "antigravity", "antigravity-cli"]), 0)

    def test_references_install_beside_instructions_and_follow_source_changes(self):
        agents = ["codex", "claude", "antigravity", "antigravity-cli"]
        self.run_sync(agents=agents, apply=True)
        installed = [
            self.home / folder / "references/design/examples.md"
            for folder in (".codex", ".claude", ".gemini")
        ]
        for path in installed:
            self.assertEqual(path.read_bytes(), self.reference.read_bytes())
            path.with_name("personal.md").write_bytes(b"Keep this\n")
        self.reference.write_bytes(b"Revised design examples\n")
        self.run_sync(agents=["antigravity-cli"], apply=True)
        self.run_sync(agents=agents, apply=True)
        for path in installed:
            self.assertEqual(path.read_bytes(), self.reference.read_bytes())
        self.assertEqual(self.run_sync(agents=agents), 0)
        self.reference.unlink()
        self.run_sync(agents=agents, apply=True)
        for path in installed:
            self.assertFalse(path.exists())
            self.assertEqual(path.with_name("personal.md").read_bytes(), b"Keep this\n")

    def test_reference_local_edit_blocks_update_and_explicit_replacement_backs_up(self):
        self.run_sync(apply=True)
        installed = self.home / ".codex/references/design/examples.md"
        installed.write_bytes(b"Local examples\n")
        (self.repo / "INSTRUCTIONS.md").write_bytes(b"Revised preferences\n")
        with self.assertRaises(ValueError):
            self.run_sync(apply=True)
        self.assertEqual(installed.read_bytes(), b"Local examples\n")
        self.assertEqual((self.home / ".codex/AGENTS.md").read_bytes(), b"Shared preferences\n")
        self.run_sync(apply=True, replace_existing=True)
        backups = list((self.home / ".agent-config/backups").glob("*/.codex/references/design/examples.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), b"Local examples\n")
        self.assertEqual(installed.read_bytes(), self.reference.read_bytes())

    def test_invalid_state_path_cannot_remove_an_unrelated_file(self):
        unrelated = self.home / "important.txt"
        unrelated.write_text("Keep this\n")
        state = self.home / ".agent-config" / "state.json"
        state.parent.mkdir()
        state.write_text(json.dumps({"codex": {"files": {"important.txt": "wrong"}}}))
        with self.assertRaises(ValueError):
            self.run_sync(apply=True, replace_existing=True)
        self.assertEqual(unrelated.read_text(), "Keep this\n")

    def test_antigravity_surfaces_can_update_separately(self):
        self.run_sync(agents=["antigravity", "antigravity-cli"], apply=True)
        instructions = self.repo / "INSTRUCTIONS.md"
        instructions.write_bytes(b"Second version\n")
        self.run_sync(agents=["antigravity-cli"], apply=True)
        instructions.write_bytes(b"Third version\n")
        self.run_sync(agents=["antigravity"], apply=True)
        self.assertEqual((self.home / ".gemini/GEMINI.md").read_bytes(), instructions.read_bytes())


    def test_document_limit_accepts_300_lines(self):
        instructions = self.repo / "INSTRUCTIONS.md"
        instructions.write_bytes(b"Preference\n" * 300)
        self.run_sync(apply=True)
        self.assertEqual((self.home / ".codex/AGENTS.md").read_bytes(), instructions.read_bytes())

    def test_oversized_document_blocks_all_installation(self):
        for relative in ("INSTRUCTIONS.md", "skills/example/assets/IMPLEMENTATION_PLAN.md", "references/design/examples.md"):
            with self.subTest(document=relative):
                document = self.repo / relative
                document.parent.mkdir(parents=True, exist_ok=True)
                document.write_bytes(b"Line\n" * 301)
                with self.assertRaisesRegex(ValueError, r"301 lines; maximum is 300"):
                    self.run_sync(apply=True, replace_existing=True)
                self.assertEqual(list(self.home.iterdir()), [])
                document.write_bytes(b"Shortened\n")


if __name__ == "__main__":
    unittest.main()
