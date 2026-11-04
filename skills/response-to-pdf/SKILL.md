---
name: response-to-pdf
description: "Export the preceding assistant response or supplied Markdown as a visually verified PDF, preserving content verbatim by default; optionally print the verified PDF to an explicitly confirmed local printer. Use when the user asks to save, export, make a PDF of, or print a response or Markdown document."
---

# Response To Pdf

Export assistant responses and supplied Markdown without rewriting them. PDF creation and
physical printing are separate operations.

## Non-negotiable behavior

- Treat "last response" as the most recent preceding completed assistant final answer.
  Exclude commentary, reasoning, plans, tool output, and the current user message.
- Verbatim is the default. Do not summarize, correct, retitle, preface, append, or otherwise
  rewrite the selected content unless the user explicitly requests editing.
- Prefer deterministic host transcript capture. In Codex, use `capture-codex`; it reads the
  stored `final_answer` associated with `CODEX_THREAD_ID`. Never scan unrelated tasks.
- If deterministic transcript access is unavailable, disclose that limitation. Use
  supplied Markdown, or obtain approval of a context-derived copy before rendering.
  Keep context-derived capture labeled as such; approval does not establish
  byte-for-byte identity with the original response.
- Never print as part of rendering. Create and verify the PDF first, then make a print plan,
  show its exact PDF, page count, printer, and settings, and obtain fresh explicit approval.
  An initial request that includes "print" is not the final approval.
- Submit at most one print job per approval. Never retry a failed or uncertain print job
  automatically.

## Run the deterministic helper

Use the directory containing this `SKILL.md` as `<skill-directory>`. Run all custom
Python under 3.14 through `uv`:

```text
uv run --directory <skill-directory> --python 3.14 python -m scripts.response_pdf <command>
```

Use absolute paths for all command-line file and directory arguments, and quote
paths containing spaces. `uv --directory` changes the working directory to the
skill directory before Python resolves relative paths.

Do not use an unqualified `python` executable.

## Create a PDF

1. For the preceding Codex response, capture the exact stored final answer:

   ```text
   ... capture-codex --output <source.md>
   ```

   For supplied Markdown, use the supplied file directly. For context-derived capture,
   write only the selected response to `<source.md>` and follow
   [the fallback rule](#non-negotiable-behavior) before rendering.

2. Render and verify, always requesting raster QA pages:

   ```text
   ... render --input <source.md> --output <document.pdf> --paper letter --qa-dir <qa-dir>
   ```

3. Inspect every generated QA PNG. Do not deliver a PDF with clipping, overflow, missing
   images, broken tables, unreadable code, or failed Mermaid diagrams. The helper also verifies
   the PDF structure and checks that visible source fragments remain extractable.

4. Deliver the PDF and report whether capture was deterministic or context-derived. Keep the
   Markdown source and JSON manifest beside the PDF unless the user requests PDF-only output.

For rendering behavior and limitations, read [references/rendering.md](references/rendering.md).

## Print a verified PDF

Read and follow [references/printing.md](references/printing.md) for printer selection,
SumatraPDF setup, plan validation, and execution.

Prepare the plan, show its confirmation text, obtain fresh approval, and submit one
job. Report "submitted to the Windows spooler" on success; do not claim physical
completion.

## Portability

For Codex, VS Code, and Antigravity discovery details and transcript-capture fallbacks, read
[references/portability.md](references/portability.md) only when installing, moving, or using
this skill in another host.
