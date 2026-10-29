# Shared agent configuration

One source for Ethan's instructions and shared skills across Codex, Claude Code, and Google Antigravity on Windows, macOS, and Linux.

## Contents

- `INSTRUCTIONS.md`: permanent communication, implementation, planning, and review preferences.
- `references/`: examples and supporting guidance linked from the shared instructions.
- `skills/`: portable workflows in the Agent Skills format.
- `agents/`: custom subagents. Each folder holds shared `instructions.md` and a header file per product.
- `sync.py`: previews or installs copies in the locations each agent reads.
- `verify.py`: checks source text encoding, line endings, and document lengths without changing files.

Python 3.10 or later and Git are required. The sync script uses only the Python standard library. If your machine uses `python3` instead of `python`, substitute that command below.

## First installation

Clone the private GitHub repository:

```sh
git clone https://github.com/enprogames/agent-config.git
cd agent-config
```

Preview installation for the agents on this machine:

```sh
python sync.py --agents codex claude antigravity
```

Select the agents you use and keep the same `--agents` selection for preview and installation. Include `antigravity-cli` for the CLI's additional skills location. A preview never changes installed configuration.

If the preview reports an existing instruction, reference, or skill file, compare it with the shared source and consolidate preferences before proceeding. First installation can explicitly back up and replace those files:

```sh
python sync.py --agents codex claude antigravity --apply --replace-existing
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

| Agent option | Global instructions | Global skills | Custom agents |
| --- | --- | --- | --- |
| `codex` | `~/.codex/AGENTS.md` | `~/.agents/skills/` | `~/.codex/agents/` |
| `claude` | `~/.claude/CLAUDE.md` | `~/.claude/skills/` | `~/.claude/agents/` |
| `antigravity` | `~/.gemini/GEMINI.md` | `~/.gemini/config/skills/` | `~/.gemini/config/agents/` |
| `antigravity-cli` | `~/.gemini/GEMINI.md` | `~/.gemini/antigravity-cli/skills/` | `~/.gemini/config/agents/` |

References are installed in a `references/` directory beside each global instruction file: `~/.codex/references/`, `~/.claude/references/`, or `~/.gemini/references/`. This preserves relative links from the instructions. References use the same conflict checks, backups, and removal rules as other managed files.

Each custom agent is a folder under `agents/` with a shared `instructions.md` and one header file per product: `codex.toml`, `claude.md`, or `antigravity.md`. Sync installs the agent only for products whose header exists. For Codex it appends the instructions as a `developer_instructions` TOML literal string, so `instructions.md` cannot contain `'''`; for the other products it appends them after the Markdown frontmatter. Codex ignores sandbox settings in agent files, so a Codex agent's read-only behavior depends on its instructions.

These are standard locations for local sessions. A custom Codex home, managed installation, cloud session, or container may need its own installation procedure. Runtime permissions, account credentials, model choices, conversation history, and machine-specific configuration stay outside this repository. Identical instructions do not guarantee identical behavior from different models.

## Project-specific guidance

Keep project build commands, architecture, and conventions in that project's `AGENTS.md`. A neighboring `CLAUDE.md` containing `@AGENTS.md` can import it explicitly for Claude Code.

The `plan-and-implement` workflow is explicit-only. Request it by name; in Codex, invoke `$plan-and-implement`. The skill's `agents/openai.yaml` disables implicit invocation in Codex, and the shared instructions require explicit agreement before any agent starts the workflow. Creating or editing the skill does not invoke it.

Only when that workflow is requested, keep its specification, design decision register, and implementation outline in one `IMPLEMENTATION_PLAN.md` with the feature's code and branch. The template is bundled under the skill's `assets/` directory. This configuration repository does not require its own planning or status document.

Skill instructions should use portable language and relative paths to bundled resources. Skills that depend on a particular product's tools or an external executable need an explicit dependency or a product-specific version.

## Check instruction loading and behavior

A successful `python sync.py --agents codex --check` confirms that managed
Codex files match the source. Use the appropriate `--agents` selection for other
clients. This does not prove that an agent loaded the files or followed their
advice.
After an authorized installation, start a fresh session and use the client's
context diagnostics, where available, to check which shared and project
instructions were loaded. A skill name in a selector does not prove that its
body or supporting references were read.

Use the [manual behavioral checks](references/design-agreement-examples.md#manual-behavioral-checks)
to assess candid advice and faithful execution. For execution cases, use a
disposable workspace. Keep the prompts and starting files consistent when
comparing instruction changes, repeat multi-turn pressure cases, and record
the agent/model version, date, loaded instructions, and observed outcomes.
Distinguish a changed factual assessment from compliance with a user choice.

The Python checks below validate file handling and distribution, not these
conversation outcomes. Do not claim cross-agent reliability from one passing
conversation. The shared agreement does not activate `plan-and-implement`;
invoke that workflow explicitly only for scenarios that need it.

## Development

```sh
python verify.py
python -m unittest discover -s tests -v
```

Tests use temporary home directories and do not change your installed agent configuration. Installation preflights conflicts across all selected files; filesystem failures during the write phase can still leave a partial update. Fix the reported filesystem issue and rerun the command.

Verification requires UTF-8 without a byte-order mark (BOM), LF line endings, a final newline for nonempty text files, and at most 300 lines per Markdown document. It checks `.md`, `.py`, `.ps1`, `.sh`, `.yaml`, `.yml`, `.json`, `.toml`, `.txt`, `.gitattributes`, `.gitignore`, and `.editorconfig` files. It skips `.git`, `.venv`, `.pytest_cache`, `.ruff_cache`, and `__pycache__` directories and unsupported file types, including binary assets. Sync skips the same directories when installing references and skills.

The verifier reports file-specific errors and exits with `1` on failure or `0` on success. Sync uses the same verification before changing installed files. GitHub checks run verification and tests on pushes and pull requests.

## Reference documentation

- [Codex global instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code instructions](https://code.claude.com/docs/en/memory)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Antigravity rules](https://antigravity.google/docs/rules/)
- [Antigravity skills](https://antigravity.google/docs/skills)
