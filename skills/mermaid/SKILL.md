---
name: mermaid
description: Check that Mermaid diagrams parse, render, and read clearly. Use whenever writing, editing, reviewing, or delivering a Mermaid diagram in any file, document, or response.
---

# Mermaid

Verify every Mermaid diagram by rendering it, then look at the result. Writing plausible
Mermaid text is not evidence that it renders.

## Workflow

1. Write the diagram. Quote labels that contain punctuation such as parentheses, brackets,
   colons, or quotes: `A["Parse (strict)"]`. When the reader's viewer is known, such as
   GitHub, VS Code, Obsidian, or a chat client, prefer long-established syntax; each viewer
   bundles its own Mermaid version.
2. Save the diagram to a file. Check diagrams in Markdown where they live. For a diagram in a
   chat response, write it to a temporary `.mmd` file outside the user's project.
3. Run the checker. Use the directory containing this `SKILL.md` as `<skill-directory>`.

   Use absolute paths for all command-line file and directory arguments, and quote
   paths containing spaces. `uv --directory` changes the working directory to the
   skill directory before Python resolves relative paths.

   ```text
   uv run --directory <skill-directory> --python 3.13 python -m scripts.mermaid_check <file>... --out-dir <png-directory>
   ```

   Inputs may be Markdown files (`.md`, `.markdown`), whose ```` ```mermaid ```` blocks are
   checked, or Mermaid files (`.mmd`, `.mermaid`), each containing one diagram. Add
   `--theme neutral`, `dark`, `forest`, or `base` to match the destination's theme.
4. Fix every failed diagram and rerun until all pass. Error line numbers refer to the input
   file.
5. Open every PNG and inspect it. Check that text is not clipped or overlapping, edges and
   labels are legible, the layout direction suits the content, and the diagram shows what
   the surrounding text claims. A misspelled node ID silently creates a new node; rendering
   cannot catch that, so compare nodes and edges with the intended structure. Revise and
   rerun when the diagram does not communicate clearly.
6. Report that the diagrams were rendered with Mermaid and visually inspected. If a check
   could not run, say which one and why. Never claim an unchecked diagram was verified.

## Output and exit codes

The checker prints JSON with the Mermaid version, the browser, and one entry per diagram:
file, diagram number, first source line, `rendered` or `failed`, and the PNG path or error.
Exit code `0` means every diagram rendered, `1` means at least one failed, and `2` means the
check could not run, for example because no diagrams were found or no browser is available.

## Limits and requirements

- Passing proves rendering with the pinned Mermaid version in a local Chromium browser. A
  viewer with an older or newer Mermaid version may still reject or draw the diagram
  differently.
- Requires `uv`, Python 3.13 or later, and Microsoft Edge or Google Chrome. Set
  `MERMAID_CHECK_BROWSER` to a Chromium executable when neither is found. The first run
  downloads the Python packages.

## Shared bundle

`assets/mermaid.min.js` is the only copy of Mermaid in these skills; `assets/versions.json`
records its version and SHA-256 hash, and the checker refuses a file that does not match.
Other skills installed beside this one load the bundle from here. To update Mermaid, replace
the bundle and its license, update `versions.json`, run this skill's tests, and render a
document with each skill that uses the bundle.
