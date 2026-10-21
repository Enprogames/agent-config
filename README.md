# Shared agent configuration

One source for Ethan's instructions and shared skills across Codex, Claude Code, and Google Antigravity on Windows, macOS, and Linux.

## Contents

- `INSTRUCTIONS.md`: permanent communication, implementation, planning, and review preferences.
- `skills/`: portable workflows in the Agent Skills format.
- `sync.py`: previews or installs copies in the locations each agent reads.
- `IMPLEMENTATION_PLAN.md`: setup status and deferred improvements.

Python 3.10 or later and Git are required. The sync script uses only the Python standard library. If your machine uses `python3` instead of `python`, substitute that command below.

## First installation

Clone the private GitHub repository once it has been published:

```sh
git clone https://github.com/enprogames/agent-config.git
cd agent-config
```

Preview installation for the agents on this machine:

```sh
python sync.py --agents codex claude antigravity
```

Use `antigravity-cli` for the CLI's additional skills location. You can select several agents, or just one. A preview never changes installed configuration.

If the preview reports an existing instruction or skill file, compare it with the shared source and consolidate preferences before proceeding. First installation can explicitly back up and replace those files:

```sh
python sync.py --agents codex --apply --replace-existing
```

For an installation without conflicts, omit `--replace-existing`. Backups are stored under `~/.agent-config/backups/`. The script records hashes in `~/.agent-config/state.json`, refuses to overwrite later local edits without explicit replacement, and preserves unrelated files. Removed shared files are removed only when they were previously installed by this script; empty directories may remain.

Start a new agent session after installation. Check that its global instruction file and the `plan-and-implement` and `review-code` skills appear in the agent's loaded instructions or skill list. Check for older global instruction files and duplicated skill names separately: this script does not rewrite other rules, plugins, or memory.

## Update every machine

Edit the source files in this repository, review the diff, then commit and push. Installed copies are generated files; make durable changes in the source.

On each other machine, use:

```sh
python sync.py --agents codex claude antigravity --pull --apply
```

`--pull` requires a clean checkout and runs `git pull --ff-only`; it does not commit, push, stash changes, or resolve conflicts. Run it only after the GitHub remote exists. Without `--pull`, installation works offline from the current checkout. The output prints the source commit so machines can compare revisions.

Check installed content without changing it:

```sh
python sync.py --agents codex --check
```

Exit codes: `0` means success or a matching check, `1` means a check found differences, and `2` means installation was blocked or failed. Matching content checks cover the selected files, while the printed source commit identifies their source revision. Source files should be committed before distribution.

## Installation locations

`~` means the current user's home directory; the script resolves it on each machine.

| Agent option | Global instructions | Global skills |
| --- | --- | --- |
| `codex` | `~/.codex/AGENTS.md` | `~/.agents/skills/` |
| `claude` | `~/.claude/CLAUDE.md` | `~/.claude/skills/` |
| `antigravity` | `~/.gemini/GEMINI.md` | `~/.gemini/config/skills/` |
| `antigravity-cli` | `~/.gemini/GEMINI.md` | `~/.gemini/antigravity-cli/skills/` |

These are standard locations for local sessions. A custom Codex home, managed installation, cloud session, or container may need its own installation procedure. Runtime permissions, account credentials, model choices, conversation history, and machine-specific configuration stay outside this repository. Identical instructions do not guarantee identical behavior from different models.

## Project-specific guidance

Keep project build commands, architecture, and conventions in that project's `AGENTS.md`. A neighboring `CLAUDE.md` containing `@AGENTS.md` can import it explicitly for Claude Code. Keep the project's living `IMPLEMENTATION_PLAN.md` with its code and branch, rather than in this global configuration repository.

Skill instructions should use portable language and relative paths to bundled resources. Skills that depend on a particular product's tools or an external executable need an explicit dependency or a product-specific version.

## Development

```sh
python -m unittest discover -s tests -v
```

Tests use temporary home directories and do not change your installed agent configuration. Installation preflights conflicts across all selected files; filesystem failures during the write phase can still leave a partial update. Fix the reported filesystem issue and rerun the command.

## Reference documentation

- [Codex global instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code instructions](https://code.claude.com/docs/en/memory)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Antigravity rules](https://antigravity.google/docs/rules/)
- [Antigravity skills](https://antigravity.google/docs/skills)
