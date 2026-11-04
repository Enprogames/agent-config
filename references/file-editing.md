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

**Starting state:** A file contains staged version A plus unstaged edits B.

**Expected:** Base the candidate on A+B, so the proposed diff contains only
the additional edits C. A detached worktree starting at HEAD does not contain
this baseline automatically. Bring the relevant current working files,
including necessary untracked files, into the disposable candidate. Leave
the original files and index unchanged.

When verification needs an implemented candidate, prepare it there, run the
appropriate checks, and refine it before presentation. Show the final
candidate's complete diff and actual verification results. Do not claim tests
of an earlier candidate validate the final one.

Once the diff and results are retained in chat, remove only the candidate and
worktree artifacts created for the proposal. Do not apply and revert edits in
the user's working tree as a substitute for isolation. If someone else has
changed the candidate, preserve it and report the cleanup limitation.

**Later approval:** "Apply these changes" authorizes C. If a necessary extra
change is discovered, explain why and show the revised complete proposal for
approval before applying the deviation.

## Using these examples

Exercise these cases in a disposable workspace. Inspect the resulting files
and staged content. Passing repository format checks or unit tests alone
does not establish that an agent followed these rules.
