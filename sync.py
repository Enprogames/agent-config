"""Install this repository's shared instructions, references, skills, and custom agents into local agents."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

from verify import IGNORED_DIRECTORIES, verify_repository


# Global instructions, skills directory, custom-agents directory, and custom-agent header file.
AGENTS = {
    "codex": (".codex/AGENTS.md", ".agents/skills", ".codex/agents", "codex.toml"),
    "claude": (".claude/CLAUDE.md", ".claude/skills", ".claude/agents", "claude.md"),
    "antigravity": (".gemini/GEMINI.md", ".gemini/config/skills", ".gemini/config/agents", "antigravity.md"),
    "antigravity-cli": (".gemini/GEMINI.md", ".gemini/antigravity-cli/skills", ".gemini/config/agents", "antigravity.md"),
}


class _ManagedFileConflict(ValueError):
    """Proposed changes would overwrite or remove a pre-existing or locally edited file."""


def digest(content):
    return hashlib.sha256(content).hexdigest()


def git_revision(repo):
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted"


def target_path(home, relative, agent):
    instruction, skills, custom_agents, _ = AGENTS[agent]
    references = (Path(instruction).parent / "references").as_posix()
    if relative != instruction and not relative.startswith((skills + "/", references + "/", custom_agents + "/")):
        raise ValueError(f"Unexpected managed path: {relative}")
    target = home / relative
    if not target.resolve().is_relative_to(home.resolve()):
        raise ValueError(f"Managed path leaves the home directory: {relative}")
    return target


def custom_agent(folder, header_name):
    """Join a custom agent's product header and shared instructions in that product's format."""
    header = (folder / header_name).read_bytes()
    instructions = (folder / "instructions.md").read_bytes()
    if header_name.endswith(".toml"):
        # A TOML literal string keeps the instructions unescaped but cannot contain its delimiter.
        if b"'''" in instructions:
            raise ValueError(f"{folder.name}/instructions.md cannot contain ''' for a Codex agent.")
        return header + b"\ndeveloper_instructions = '''\n" + instructions + b"'''\n"
    return header + b"\n" + instructions


def desired_files(repo, agents):
    instructions = (repo / "INSTRUCTIONS.md").read_bytes()
    desired = {}
    for agent in agents:
        instruction, skills, custom_agents, header_name = AGENTS[agent]
        files = {instruction: instructions}
        references = Path(instruction).parent / "references"
        for source in sorted((repo / "references").rglob("*")):
            if source.is_file() and IGNORED_DIRECTORIES.isdisjoint(source.relative_to(repo).parts):
                relative = source.relative_to(repo / "references")
                files[(references / relative).as_posix()] = source.read_bytes()
        for manifest in sorted((repo / "skills").glob("*/SKILL.md")):
            folder = manifest.parent
            for source in sorted(folder.rglob("*")):
                if source.is_file() and IGNORED_DIRECTORIES.isdisjoint(source.relative_to(repo).parts):
                    relative = source.relative_to(repo / "skills").as_posix()
                    files[f"{skills}/{relative}"] = source.read_bytes()
        # Each agent folder supports the products whose header file it contains.
        for header in sorted((repo / "agents").glob(f"*/{header_name}")):
            folder = header.parent
            files[f"{custom_agents}/{folder.name}{header.suffix}"] = custom_agent(folder, header_name)
        desired[agent] = files
    return desired


def sync(repo, home, agents, apply=False, replace_existing=False):
    errors = verify_repository(repo)
    if errors:
        raise ValueError("Repository verification failed:\n" + "\n".join(errors))
    state_path = home / ".agent-config" / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    desired = desired_files(repo, agents)
    changes = {}
    conflicts = []

    # Check the complete operation before changing any installed file.
    for agent, files in desired.items():
        previous = state.get(agent, {}).get("files", {})
        for relative in sorted(set(files) | set(previous)):
            target = target_path(home, relative, agent)
            if target.exists() and not target.is_file():
                raise ValueError(f"Expected a file: {target}")
            current = target.read_bytes() if target.exists() else None
            wanted = files.get(relative)
            if current == wanted:
                continue
            # Antigravity's app and CLI can update their shared instruction separately.
            previous_hashes = {
                installed.get("files", {}).get(relative) for installed in state.values()
            }
            changed_locally = current is not None and digest(current) not in previous_hashes
            if changed_locally and not replace_existing:
                conflicts.append(str(target))
            # Two Antigravity surfaces share the same global instruction file.
            changes[relative] = (target, wanted, current, changed_locally)

    if conflicts:
        raise _ManagedFileConflict(
            "Existing or locally edited files need review:\n  "
            + "\n  ".join(sorted(set(conflicts)))
            + "\nUse --replace-existing only after review; it saves backups."
        )

    for relative, (_, content, _, _) in changes.items():
        print(f"{'REMOVE' if content is None else 'WRITE '} {relative}")
    revision = git_revision(repo)
    print(f"Checkout Git HEAD: {revision}")
    if not apply:
        if replace_existing:
            print("Preview only; no changes applied. Add --apply to install with --replace-existing.")
        else:
            print("Preview only; no installed files changed.")
        return len(changes)

    backup_root = home / ".agent-config" / "backups" / datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%S%fZ")
    for relative, (target, content, current, changed_locally) in changes.items():
        if changed_locally:
            backup = backup_root / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(current)
            print(f"BACKUP {backup}")
        if content is None:
            target.unlink()
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)

    for agent, files in desired.items():
        state[agent] = {
            "revision": revision,
            "files": {relative: digest(content) for relative, content in files.items()},
        }
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print("Installed. Start a new agent session to load the instructions.")
    return len(changes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", nargs="+", choices=AGENTS, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Install the previewed changes")
    mode.add_argument("--check", action="store_true", help="Exit 1 if installed files differ, including conflicts")
    parser.add_argument("--pull", action="store_true", help="First git pull --ff-only; requires a clean checkout")
    parser.add_argument("--replace-existing", action="store_true", help="Back up and replace existing or locally edited managed files")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent
    try:
        if args.pull:
            status = subprocess.run(
                ["git", "-C", str(repo), "status", "--porcelain"],
                check=True, capture_output=True, text=True,
            )
            if status.stdout.strip():
                raise ValueError("Commit or resolve source changes before --pull.")
            subprocess.run(["git", "-C", str(repo), "pull", "--ff-only"], check=True)
        changes = sync(repo, Path.home(), list(dict.fromkeys(args.agents)), args.apply, args.replace_existing)
        return 1 if args.check and changes else 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        if args.check and isinstance(error, _ManagedFileConflict):
            print(error, file=sys.stderr)
            return 1
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
