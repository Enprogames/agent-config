# Technical Authoring Standard

## Reader contract

Before drafting, establish what the reader should understand, decide, change, build, or
debug after reading. State prerequisites when their absence would block understanding,
but do not bury the document under introductory material the intended reader does not
need. Keep adjacent topics out of scope unless they are necessary to complete the reader's
task.

## Progressive fidelity

Make a difficult subject approachable without making it falsely simple:

1. Begin with an accurate orientation or first-pass mental model.
2. Say where that model is simplified when the limitation could mislead the reader.
3. Introduce exact terminology, notation, components, or states near first use.
4. Work through a concrete example that connects the important parts end to end.
5. Expose deeper mechanics, assumptions, invariants, edge cases, and failure modes.
6. Provide the practical or reference information the intended reader will revisit.

The opening should help a beginner enter the subject; later sections should withstand an
expert's scrutiny. Do not create duplicate beginner and expert explanations when one
layered explanation can serve both. In annotated source reports, arrange source passages
to provide this progression and add clearly separated explanations where needed. Apply
the prose guidance below to agent annotations without rewriting the quoted source text.

## Prose

- Write like a careful senior engineer or teacher speaking to a capable reader.
- Prefer concrete subjects, active verbs, exact nouns, and short purposeful paragraphs.
- Replace vague pointers such as "this," "it," "various," or "works somehow" when the
  referent or mechanism is not immediately clear.
- Explain why a mechanism exists, what enters it, what changes, what leaves it, and what
  can fail when those facts help the reader reason about the system.
- Put examples and qualifications close to the claims they clarify.
- Use domain vocabulary directly, but define unfamiliar terms before relying on them.
- Prefer useful transitions over repeated summaries.
- Remove hype, self-congratulation, unearned adjectives, and metadiscourse about the
  document being comprehensive, robust, elegant, or important.
- End with practical guidance, a reference, an unresolved boundary, or the natural end of
  the explanation. Do not add a ceremonial conclusion.

## Structure and navigation

Use headings that reveal the reader's path and make sections independently findable.
Include a table of contents only when length or non-linear use justifies it. Use bullets
for scanning, numbered lists for real sequences, and tables for exact comparisons or
repeated-field mappings. Avoid one-sentence heading forests and large unbroken sections.

Keep the document standalone enough for its audience. Link to deeper material when useful,
but do not make readers chase several planning documents merely to understand the core
subject.

## Precision

Use exact names, units, ranges, dates, addresses, equations, bit masks, timing boundaries,
commands, and versions when they affect behavior. Define symbols before using them and
check dimensional or unit consistency. Separate guarantees from typical observations and
current behavior from future-looking design.

Length should follow the subject. Be locally concise, but spend words where they prevent
misunderstanding, reveal a hidden constraint, or make the document genuinely usable.
