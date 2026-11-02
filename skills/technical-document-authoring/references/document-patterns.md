# Document Patterns

Treat these as menus, not templates. Include only sections that help the current reader.

## Research report modes

Resolve the mode before research using the explicit request and applicable user defaults.
The modes share evidence standards; they differ in who supplies the explanatory narrative.
Keep audience, depth, and task purpose as parameters rather than creating additional modes.
These modes do not force quick answers, code walkthroughs, or other documents into reports.

### Annotated source report

Teach the central technical content through verbatim passages. Select complete explanatory
units, often paragraphs or connected paragraphs where permitted. Avoid isolated quotations
that merely decorate an agent-written explanation. Keep original introductions,
transitions, and conclusions brief; do not impose a quotation percentage or word ratio.

For each substantive section:

1. Briefly identify the question or concept.
2. Name the source and present the relevant passage in a blockquote. Include title,
   author or responsible organization when known, source type, direct link, and a useful
   locator; include date or version when relevant. Shorten repeated source labels.
3. Assess comprehension against the intended reader's knowledge. Immediately explain
   dense reasoning, unfamiliar terms or notation, ambiguous phrases, hidden prerequisites,
   or missing context. Use takeaway bullets, background, definitions, or a worked example
   as needed; do not add every category after every excerpt.
4. State material source limitations or unresolved disagreements near the affected passage.

Label annotations **Agent explanation** or **Agent interpretation** and make clear which
passage they address. Keep them outside the quotation. Added factual background needs
its own evidence; label illustrative examples. Minimize unnecessary narration without
sacrificing comprehension, even when a difficult passage needs a longer explanation.

Example request: "Write about aspect Y of technical topic X using
source-grounded-research and technical-document-authoring." With an annotated-report
default, arrange teaching passages about Y and explain their difficult parts; do not
deliver an original essay with a few supporting quotations.

### Synthesized report

Use agent-written explanation and analysis when the requested outcome calls for synthesis.
Name important sources in the prose and cite specific supporting passages or sections
near factual claims. Use selected excerpts when exact wording matters or helps the reader
audit important reasoning. Keep source claims, agent interpretations, and recommendations
visibly distinct; do not imply that a source states the agent's combined conclusion.
State concrete material source concerns where the evidence is used.

Example request: "Compare approaches A and B and recommend one for workload C." Explain
the comparison with precise evidence and identify the recommendation as agent judgment
unless a cited source explicitly makes that recommendation for the relevant conditions.

### Limits and handoff

Follow [excerpt handling](figures-and-code.md#source-excerpts) for verification and quotation
limits. If the requested excerpt coverage cannot be provided, disclose the restriction
and give permitted excerpts with precise passage links or locators. Do not silently
switch modes. Preserve mode, actual passages, attribution, and caveats across handoffs.

## Conceptual or mathematical explainer

- the question the concept answers;
- an intuitive but bounded mental model;
- definitions and notation;
- a small worked example;
- the general mechanism or derivation;
- assumptions and what happens when they fail;
- implementation or application guidance;
- a compact reference for formulas, terms, or decisions.

When mathematics matters, move from concrete values to symbols and from a small case to
the general case. Explain what quantities mean, not only how equations transform them.

## Low-level system behavior

- scope and observable behavior;
- components, state, and ownership boundaries;
- ordering, timing, or lifecycle;
- important data representations and transformations;
- invariants and edge cases;
- evidence and verification strategy;
- consequences for implementation or debugging.

Use precise diagrams or timelines when ordering cannot be understood reliably from prose.

## Code walkthrough

- the user-visible or system outcome;
- the entry point and a small component map;
- the end-to-end control and data path;
- key branches, state changes, and invariants;
- error, retry, cancellation, or cleanup behavior;
- where common changes belong;
- how to verify or debug the workflow.

Trace actual code. Cite files and symbols, show representative snippets, and distinguish a
documented design from the current implementation.

## Service or platform explanation

- the public contract and boundary;
- request or lifecycle model;
- execution, isolation, concurrency, and state where relevant;
- limits and context-dependent behavior;
- failures, retries, idempotency, and recovery;
- observability, security, cost, and operational tradeoffs;
- current source context for changeable claims.

Separate public guarantees from implementation details and typical observations.

## Architecture note

- the problem and constraints;
- the system boundary and major responsibilities;
- data, control, and dependency direction;
- decisions and tradeoffs;
- important runtime flows;
- failure modes and operational consequences;
- extension points and verification.

## Implementation guide or plan

- target behavior and success conditions;
- constraints, decisions, and work boundaries;
- affected components and representative changes;
- migration or sequencing when order matters;
- validation intent;
- unresolved questions and risks.

Describe the desired durable state. Do not narrate completed work unless the user requests
a worklog or release note.

## Reference material

Optimize for lookup rather than linear reading. Use stable terminology, descriptive
anchors, exact mappings, compact examples, and cross-references. A glossary, table, or
index is appropriate when it materially reduces search effort; none is required by
default.
