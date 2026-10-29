---
name: technical-document-authoring
description: Draft, revise, or review source-grounded technical explanations, developer documentation, code walkthroughs, architecture notes, and reference material. Use when writing must be clear to beginners, technically deep, skimmable, code-aware, and supported by purposeful citations, examples, or visuals. Do not use for nontechnical writing or document-formatting-only work.
---

# Technical Document Authoring

Create technical documents that readers can enter quickly, understand accurately, and
return to as reference material. Optimize for sentence-level clarity and document-level
depth rather than arbitrary brevity.

## Authoring Workflow

1. Establish the reader contract: intended audience, assumed knowledge, desired outcome,
   scope, and relevant constraints.
2. Build the evidence base. Inspect supplied material and relevant repository files
   before describing them. Use the `source-grounded-research` skill when important claims are
   current, disputed, correctness-sensitive, externally sourced, or not adequately
   supported by the available material. Do not launch deep research for a small prose
   edit whose facts are already established.
3. Choose a reader journey rather than imposing a stock report template. For substantial
   documents, use [references/document-patterns.md](references/document-patterns.md) as
   a menu of useful shapes.
4. Draft with progressive fidelity: give the reader a useful first mental model, label
   its simplifications, and then expose the exact mechanics, constraints, evidence, and
   edge cases. Follow [references/authoring-standard.md](references/authoring-standard.md).
5. Add excerpts, code, tables, Mermaid, visualizations, or images only when they improve
   comprehension, verification, comparison, navigation, or recall. When any are used,
   read [references/figures-and-code.md](references/figures-and-code.md). Check and
   inspect each Mermaid diagram with the `mermaid` skill.
6. Perform the independent quality passes in
   [references/quality-review.md](references/quality-review.md). Repair problems rather
   than merely listing them.
7. Validate substantial Markdown and visually inspect rich documents as described below.

## Grounding and Honesty

- Cite important external claims near the text they support.
- Prefer real file, symbol, command, API, and type names. Do not invent repository facts.
- Separate observed, documented, inferred, proposed, tested, and untested statements.
- Preserve an evidence pack's scope, confidence, and caveats. Return to research if the
  desired wording would require a stronger claim than the evidence supports.
- If documentation and implementation disagree, identify the disagreement and the basis
  used for the current explanation.
- Do not imply that a command, test, source, link, render, or image was checked when it
  was not.

## Editing Existing Documents

Preserve the document's purpose, audience, and useful structure. Make the smallest
semantic change that leaves it accurate. Prefer replacing or deleting stale text over
appending qualifications, implementation history, or changelog noise. Reread the result
as ordinary prose without the diff and remove repetition.

Do not turn canonical documentation into a worklog, test transcript, task list, or agent
narrative unless the user asks for that deliverable. Create or edit files only when the
request authorizes it.

## Markdown QA

For a substantial Markdown document, run the deterministic structural validator:

```text
uv run --directory <skill-directory> --python 3.13 python -m scripts.markdown_qa validate --input <document.md> [--manifest <manifest.json>]
```

Add `--render --qa-dir <directory>` when the document contains Mermaid, images, complex
tables, long code, or other layout-sensitive content. Add `--allow-remote-assets` only
when remote images are required and network access is authorized. Inspect every generated
PNG; the manifest deliberately records that visual inspection remains required.

The helper checks structure, local links and anchors, image assets and alt text, heading
hierarchy, code fences, Mermaid parsing and SVG production, browser overflow, and broken
rendered images. It does not check the factual quality of prose, compile arbitrary code,
or prove that external URLs are reachable.

When the requested deliverable is PDF, Word, a site, or another rendered format, also use
that format's native render-and-inspect workflow. Markdown preview does not prove the
final artifact is correct.
