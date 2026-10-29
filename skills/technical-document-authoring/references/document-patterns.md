# Document Patterns

Treat these as menus, not templates. Include only sections that help the current reader.

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
