# Editing files without disturbing the user's work

These examples support the shared file-editing rules in INSTRUCTIONS.md.

## Example 1: Editing a partially staged file

**Before:** The user staged version A, then made additional unstaged edits.

**Request:** Change one validation message.

**Expected:** Edit the current file on disk, retaining the user's other edits.
Leave version A staged. `git diff` shows the user's existing unstaged edits
and the agent's new changes relative to A.

Do not rebuild the file from HEAD or the staged version, rewrite the staging
area directly, or stage changes to make the diff easier to read.

**Check:** Compare `git diff --cached --binary --no-ext-diff` before and after
editing to confirm staged content is unchanged. Review `git diff` to confirm
the requested change and preservation of the user's other edits.

**If the user later says "Commit these changes":** That authorizes staging the
specified changes as needed and committing them. Preserve unrelated staged
and unstaged changes and leave them out of the commit.

## Example 2: Preserving an existing file's format

**Before:** A file uses UTF-8 without BOM, CRLF line endings, and no final
newline.

**Request:** Replace an error message.

**Expected:** Change the message while retaining UTF-8 without BOM, CRLF
endings, and no final newline. New-file defaults do not authorize converting
this file to LF or adding a terminating newline.

**Check:** Inspect the original and resulting bytes to confirm the encoding,
BOM presence, line endings, and file ending are preserved. Choose an editing
method that retains those properties; do not assume a tool's defaults match
the file.

If a formatting check finds an existing issue, report it. Do not silently
convert unrelated files to make the check pass.

## Previewing changes before approval

**Request:** "Show me the before/after changes you recommend."

**Starting state:** The working files may contain changes that have not been
staged.

### Prepare and verify the candidate

Use the files as they exist on disk as the baseline unless the
user requests another comparison. Use a task-owned temporary workspace. For
Git, default to a detached worktree and record its absolute path and starting
commit. Copy in the relevant working-file edits and any needed untracked
inputs. Diff against that snapshot so the patch contains only the proposal.
Keep the original checkout and index intact.

Run the relevant build and targeted tests for code changes,
including applicable existing tests and any tests added or changed. Use the
project's applicable checks for other changes. Isolate writable test state
and build outputs. Report the checks, results, and limitations for the final
candidate.

### Preserve the verified patch

Capture the exact patch and verification results before cleanup.
Check that the patch reproduces the final candidate from the baseline. If
later application requires an internal copy, keep the patch and necessary
baseline details outside both checkouts. Remove that copy once the proposal
is applied, declined, or superseded.

### Remove the temporary workspace

Before presenting the preview, stop the candidate's processes and leave its
directory. Do this after success or failure, and after cancellation when
execution is still available. Remove only the checkout and temporary outputs
owned by the preview. For Git, use `git worktree remove` on the recorded path. Use
`--force` only if the remaining tracked, untracked, and ignored contents are
known to be disposable. Preserve unexpected edits and any checkout the user
asked to keep. Verify the directory is gone and, for Git, the registration is
absent from `git worktree list --porcelain`. Report the result. If cleanup is
blocked, give the exact path, what remains, and why.

### Recheck before applying

"Apply these changes" authorizes the proposed diff.
Check that it still applies to the intended checkout and preserves any
intervening edits. If a necessary extra change is discovered, explain why and
show the revised complete proposal for approval before applying the deviation.

## Applying changes "as planned"

**Request:** "Edit the current working tree files as planned."

**Expected:** Identify the specific patch or plan being approved from the
conversation and proceed without redundant confirmation. This request can
itself grant approval; separate approval wording is not required.

If the user is approving a complete diff, apply those exact edits. Calling
them "planned changes" does not authorize an alternative implementation.

If the user is approving an implementation plan without a complete diff,
follow its specified behavior, design, scope, and review checkpoints. Resolve
routine coding details within those boundaries. Proposed or deferred
alternatives remain unapproved.

If the conversation leaves materially different plans as plausible referents,
ask which one the user means before making dependent edits.

Edit the current working files, preserving existing user edits and staged
content. Run the agreed checks. If completing the work requires departing
from the applicable approval, explain why and obtain approval for the
revision before applying that deviation.

## Using these examples

Exercise these cases in a disposable workspace. Inspect the resulting files
and staged content. Passing repository format checks or unit tests alone
does not establish that an agent followed these rules.
