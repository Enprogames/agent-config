---
name: source-grounded-research
description: Investigate questions using authoritative, claim-appropriate sources and produce traceable evidence. Use for deep research, precise citations or excerpts, current or disputed claims, comparison of sources, codebase investigation, or evidence needed for a document. Do not use when the supplied evidence is sufficient and the user only needs editing or summarization.
---

# Source Grounded Research

Establish what is known, how it is known, and where uncertainty remains. Adapt the
depth and visible structure to the request; the research method is a quality control,
not a mandatory report template.

## Research Method

1. Define the question, audience, scope, and any context that could materially change
   the answer, such as date, jurisdiction, edition, implementation, environment, or
   release. Include only context that is relevant.
2. Inspect supplied material and relevant local files before looking elsewhere.
3. Identify the important claims the answer must establish. Research those claims
   rather than collecting sources indiscriminately.
4. Select evidence according to the claim. Prefer sources closest to the underlying
   facts and use independent corroboration when a material claim is ambiguous,
   disputed, surprising, or costly to get wrong.
5. Record provenance and caveats while researching. For substantial investigations,
   use the evidence-pack contract in [references/evidence-pack.md](references/evidence-pack.md).
6. Reconcile disagreements by checking scope, terminology, assumptions, methods,
   dates, and versions. Do not manufacture consensus.
7. Answer at the confidence supported by the evidence and state material unknowns.

Read [references/source-evaluation.md](references/source-evaluation.md) when choosing
among competing sources, handling current or disputed claims, or using excerpts.

## Evidence Discipline

- Distinguish confirmed facts from inference, hypothesis, and recommendation.
- Distinguish primary evidence from secondary interpretation, documented claims from
  observed results, and current information from historical or superseded information.
- Treat source authority as claim-relative. A respected source outside its competence
  is not automatically strong evidence.
- Prefer direct pages, records, papers, datasets, repositories, and specifications over
  search snippets or unsourced summaries.
- Cite important external claims near the text they support. Use locators such as page,
  section, table, figure, symbol, or commit when they materially improve verification.
- Use short excerpts to establish exact wording or resolve ambiguity. Explain what each
  excerpt proves; do not build the answer from quotation piles.
- When inspecting a codebase, cite real files and symbols and separate current behavior
  from intended, documented, or proposed behavior.
- Do not claim that a source, command, test, or artifact was inspected when it was not.

## Output

Lead with the answer or finding most useful to the reader. Expose the evidence ledger
only when the user requests it or when the subject's uncertainty makes it useful.
Otherwise integrate citations, caveats, and concise source excerpts into a readable
answer or pass an evidence pack to the document-authoring workflow.

Stop when the important claims are adequately supported for the requested stakes and
remaining uncertainty is explicit. Do not continue browsing merely to accumulate more
sources.

Do not change code, documents, external systems, or records unless the user separately
asks for those changes.
