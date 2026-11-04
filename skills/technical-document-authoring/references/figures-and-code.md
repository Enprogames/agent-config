# Excerpts, Code, and Visuals

Add media because it performs a job, not to satisfy a quota. The smallest useful visual is
usually the best one.

## Source excerpts

Choose excerpts for the [report mode](document-patterns.md#research-report-modes):
annotated source reports use teaching passages; synthesized reports use selected excerpts
to clarify wording or expose the basis for analysis. Identify sources beside their
passages and separate quotations from agent explanations.

For quotation verification, attribution, and quotation limits, read and follow
[the source-grounded-research excerpt rules](../../source-grounded-research/references/source-evaluation.md#excerpts-and-citations).

## Code snippets

- Prefer real repository code when explaining current behavior.
- Identify the file and symbol; include a revision when the snapshot matters.
- Preserve enough context to understand types, state, inputs, and outputs.
- Use short representative excerpts instead of dumping implementations.
- Mark omissions, pseudocode, and hypothetical or illustrative code explicitly.
- Test, compile, or otherwise verify illustrative code when feasible and useful.
- Explain the decision point, invariant, transformation, or failure behavior the snippet
  reveals. Do not merely restate each line.
- Use before/after snippets only for an actual comparison or proposal.

## Choosing a visual

- **Table:** exact mappings, comparisons, repeated fields, or boundary conditions.
- **Flowchart:** architecture, ownership, dependencies, or data flow.
- **Sequence diagram:** runtime interactions and ordering.
- **State diagram or timeline:** lifecycle, transitions, timing, and protocol behavior.
- **Chart or plot:** quantitative relationships, distributions, uncertainty, scaling, or
  measured tradeoffs.
- **Sourced image or screenshot:** actual appearance, physical arrangement, or primary
  visual evidence.
- **Generated illustration:** conceptual or spatial intuition that cannot be expressed as
  clearly with a diagram or sourced image.

Prefer several focused diagrams to one diagram that combines unrelated ideas. Mermaid is
well suited to relationships, sequences, and states; it is not automatically the right
tool for quantitative plots, dense spatial layouts, or exact screenshots.

## Figure contract

Every figure should have:

- a specific explanatory purpose;
- a caption or title;
- source or derivation;
- alt text where the format supports it;
- units, scale, legend, and assumptions when quantitative;
- a nearby explanation and an explicit reference from the prose;
- verification that it agrees with the surrounding claims.

Generated images are illustrative, not evidence. Label them accordingly. When a diagram
is derived from external evidence, say so and cite the evidence. Do not invent visual
precision: a conceptual drawing should not masquerade as a measured plot, schematic, or
implementation trace.

## Materiality test

Remove a figure, excerpt, snippet, or table if the document remains equally understandable,
verifiable, and usable without it. If the media is necessary, ensure the surrounding prose
still explains the takeaway for readers who cannot view it.
