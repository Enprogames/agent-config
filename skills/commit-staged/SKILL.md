---
name: commit-staged
description: Propose commit messages from Git's staged changes, or commit those changes when requested. Use for requests such as "what should the commit message be?" or "commit the staged changes."
---

# Commit staged changes

1. Inspect the full staged diff with `git diff --cached --no-ext-diff --no-textconv`.
   Use index versions of partially staged files for context. If nothing is staged,
   report that and stop.
2. For suggestions, give three numbered alternatives unless asked otherwise.
   Each message must be one physical line, technically specific, and easy to read.
   Cover the main change and important behavior, varying the emphasis across options.
   Prefer concrete verbs and component names over generic claims or a file inventory.
   Follow requested or required message conventions; add no arbitrary length limit.
3. A message-only request does not authorize a commit. "Use the third suggestion"
   selects wording after a message request; commit with it when committing was
   already requested. For an explicit commit request, use the supplied message or
   choose one without another approval. If the user requested options before
   committing, wait for their choice.
4. Immediately before committing, recheck the staged diff. If its scope or behavior
   materially changed, explain the difference and refresh the proposal before proceeding.
   Commit only staged content with the exact selected message; preserve unstaged work.
   Report the recorded commit hash and message, and any remaining work.
