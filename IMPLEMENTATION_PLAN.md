# Central agent configuration

## Agreed scope

Create a private `enprogames/agent-config` GitHub repository and a local checkout containing shared instructions, portable skills, and a small installation/update command. Use generated copies in each agent's supported global locations.

Completion means the local repository is validated, published privately on GitHub, and ready to clone on other machines. Installing into each machine's agent configuration is an explicit follow-up step.

## Decisions

- Keep permanent preferences in INSTRUCTIONS.md and longer procedures in two skills: plan-and-implement and review-code.
- Use a Python standard-library script and ordinary file copies for portability across Windows, macOS, and Linux.
- Preview by default. Detect local modifications before writing. Back up conflicting files only when explicit replacement is requested.
- Keep account credentials, session state, permissions, and machine-specific configuration local.

## Progress

- [x] Inspect the currently accessible global instructions and local Git tooling.
- [x] Draft shared instructions and skills from the preferences agreed in this conversation.
- [x] Implement sync.py with selected-agent installation and optional fast-forward updates.
- [x] Run behavior tests and skill validation.
- [ ] Initialize and commit the local repository.
- [ ] Authenticate to GitHub as enprogames, create the private remote, and push.
- [ ] Verify the GitHub repository and local remote configuration.

Verification: all nine behavior tests pass using temporary home directories. Both skills pass the official skill validator. The current machine's Codex installation preview lists the instruction file and two skills without writing them.

Git Credential Manager has an existing sign-in for Enprogames. GitHub's API confirms the account and that the repository name is available. No additional sign-in is needed. Credentials remain outside this repository.

## Deferred improvements

- Install on the current machine after reviewing the preview and authorizing writes to the global agent directories.
- Add a launch shortcut that updates before starting an agent if manual updates become easy to forget.
- Add machine-specific dependency setup only when a shared skill actually needs additional software.
- Package provider-specific plugins only when direct skill copies no longer cover a required capability.
