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
   release. Include only context that is relevant. For reports, resolve the mode from
   the request and applicable user preferences before collecting evidence: an
   **annotated source report** teaches through source passages; a **synthesized report**
   presents agent analysis with citations. Other research tasks need no report mode.
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
- Collect excerpts for the chosen mode. Annotated source reports need passages that
  teach the subject, not just sentences supporting agent-written claims. Synthesized
  reports use selected excerpts where wording matters or helps audit the analysis.
  Verify quotations and context as described in the source-evaluation reference.
- When inspecting a codebase, cite real files and symbols and separate current behavior
  from intended, documented, or proposed behavior.
- Do not claim that a source, command, test, or artifact was inspected when it was not.
- Before answering, check that the code actually behaves as described, that precise
  details such as timing, bit masks, addresses, or state transitions are not
  oversimplified, and that documented behavior, design intent, and implementation
  convenience are not conflated. When recommending tests, check that they would catch
  the specific defect rather than only confirm the current implementation.

## Output

Lead with the answer or finding most useful to the reader. Expose the evidence ledger
only when the user requests it or when the subject's uncertainty makes it useful.
Preserve the chosen report mode: let source passages carry an annotated report's
substantive explanation, with clearly separated annotations where needed. In synthesized
reports, integrate precise citations and selected excerpts into the agent's analysis.
Pass the mode, actual excerpts, provenance, and caveats to the document-authoring workflow
when handing off research; do not replace teaching passages with claim summaries.

Stop when the important claims are adequately supported for the requested stakes and
remaining uncertainty is explicit. Do not continue browsing merely to accumulate more
sources.

Do not change code, documents, external systems, or records unless the user separately
asks for those changes.
