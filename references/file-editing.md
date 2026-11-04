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

**Expected:** Use the files as they exist on disk as the baseline. If an
isolated candidate is needed, copy the relevant files, including necessary
untracked files, into it and make the proposed edits there. Leave the
original working files and Git staging area unchanged.

When verification needs an implemented candidate, prepare it there, run the
appropriate checks, and refine it before presentation. Show the final
candidate's complete diff and actual verification results. Do not claim tests
of an earlier candidate validate the final one.

Once the diff and results are retained in chat, remove only the candidate and
worktree artifacts created for the proposal. Do not apply and revert edits in
the user's working tree as a substitute for isolation. If someone else has
changed the candidate, preserve it and report the cleanup limitation.

**Later approval:** "Apply these changes" authorizes the proposed diff. If a
necessary extra change is discovered, explain why and show the revised
complete proposal for approval before applying the deviation.

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
