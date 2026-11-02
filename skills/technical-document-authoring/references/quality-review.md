# Quality Review

Review the completed document in separate passes. Repair discovered problems before
delivery. These are gates, not headings to add to the document.

## Evidence

Can every important factual claim be traced to supplied material, current code, direct
observation, or a claim-appropriate external source? Are citations adjacent to the claims
they support? Are material conflicts and unknowns visible?

## Research report mode

Does the format match the explicit request or applicable user default, including across
research and authoring handoffs? In an annotated source report, can the reader learn
the central technical content from source passages, with necessary explanations visibly
separated? In a synthesized report, are important sources named, citations precise, and
source statements distinguishable from the agent's combined analysis or recommendation?

Are excerpts accurate against inspected sources, including equations and qualifiers?
Are omissions and insertions marked, separate passages kept separate, and surrounding
conditions preserved? Are source identity, useful locators, and concrete material
trustworthiness concerns visible? Are unverified assertions distinguishable from
corroborated information or reproducible observations? If quotation or access limits
prevented coverage, is that explicit rather than hidden by a change of mode?

## Correctness

Check names, equations, units, dimensions, ranges, dates, timing, bit operations, commands,
links, and context-dependent claims. Verify that examples and diagrams agree with the
prose. Separate contracts, typical observations, and implementation details.

## Pedagogy

Can the intended reader enter without hidden prerequisites? Are terms and symbols defined
before use? Does at least one example connect the important pieces? Are simplified models
labeled before they become misleading? Are dense source passages accompanied by the
takeaways, background, term definitions, or examples the intended reader needs? Is added
factual background supported without implying it is part of the quoted source?

## Depth

Has simplification erased a relevant assumption, invariant, tradeoff, edge case, or
failure mode? Does the document explain mechanisms and consequences rather than merely
name components?

## Navigation

Can a reader quickly find the mental model, exact behavior, examples, common changes,
failure guidance, and reference information that actually belong in this document? Are
headings descriptive, sections proportionate, and lists or tables used for real structure?

## Prose

Reread without the drafting history or diff. Remove repetition, vague references, filler,
hype, defensive qualifications, and generic introductions or conclusions. Prefer concrete
subjects and verbs. Keep paragraphs focused without making the document choppy.

## Media

Does every excerpt, snippet, table, diagram, chart, and image earn its space? Is it labeled,
sourced or described as derived, accessible, explained, and consistent with the evidence?
Are generated images clearly illustrative rather than evidentiary?

## Honesty

Are observed, documented, inferred, proposed, tested, and untested claims distinguishable?
Does the document avoid implying that unavailable checks were performed? Is future-looking
behavior kept separate from the current state?

## Rendering

Run structural Markdown validation for substantial Markdown. Render when diagrams, images,
tables, long code, or layout-sensitive content make visual failure plausible. Inspect every
preview image for overflow, unreadable code, broken assets, poor spacing, and diagram
legibility. Then run the native render-and-inspect workflow for the final output format.

Parsing cannot prove visual correctness, and visual inspection cannot prove source
integrity or factual accuracy. Use the relevant gates together.
