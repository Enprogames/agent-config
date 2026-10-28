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

## Using these examples

Exercise these cases in a disposable workspace. Inspect the resulting files
and staged content. Passing repository format checks or unit tests alone
does not establish that an agent followed these rules.
