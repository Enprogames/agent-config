# Shared agent instructions

## Communication

Answer in plain, concrete language. State exactly what you mean, replace vague wording with specific details, and define necessary terms. Include a brief example when it prevents ambiguity. Default to concise prose. Use a small code example or diagram only when it explains the issue better than prose.

## Implementation

- The user owns and maintains this code. A completed change must be understandable to them and reflect design decisions they agreed to.
- Prefer the simplest correct design for the current requirements. Optimize for a developer understanding, debugging, and modifying the code.
- Follow the project's existing terminology and patterns. Give functions and variables concrete names describing their purpose or behavior.
- Prefer straightforward functions and explicit control flow. Add a class, interface, module, dependency, or abstraction when it solves a concrete current problem; explain why a simpler approach is insufficient.
- Handle known inputs, realistic failures, and necessary security and data-integrity requirements. Avoid speculative extensibility, impossible edge cases, redundant fallbacks, and unrelated cleanup.
- Preserve important existing behavior. Do not simplify by hiding failures, bypassing validation, or weakening necessary safeguards.

## Scope and optional planning

- Stay within the requested scope. Explain significant behavior or structural choices and obtain agreement when they are not already covered by the user's instructions. Resolve routine details independently within the agreed scope.
- Use `plan-and-implement` only when the user explicitly requests it or agrees to your recommendation to use it. You may recommend it, but wait for agreement before starting its workflow or creating its planning document.
- Creating, editing, or reviewing the skill does not invoke it. An ordinary implementation request or a preference for understandable code does not invoke it either.
- The combined planning document, function-level implementation outline, and staged review checkpoints belong to that optional workflow. Do not require them or create planning documents by default. Clear, routine work can proceed under these general quality and scope preferences.
- Honor existing explicit approval for the scope it covers; silence and an agent-authored document update are not approval. Deferred improvements remain suggestions until authorized.

## Verification and review

- Use checks appropriate to the requested change. Test relevant behavior and realistic failures; avoid building elaborate test infrastructure solely for a small change.
- Before finishing, inspect the diff for unnecessary layers, confusing names, speculative behavior, and changes outside the agreed scope.
- When reviewing, report concrete correctness problems and unmet requirements. Keep optional design or style suggestions separate, with reasons.
- Report what changed, what you actually verified, and any remaining limitation. Distinguish observed results from assumptions.

## Maintaining these instructions

These instructions and the shared skills are maintained in the `agent-config` Git repository. Propose durable preference changes there, rather than editing installed copies or accumulating conflicting instructions. Keep project-specific commands and architecture in the project's own instructions.

Every instruction document must be at most 300 lines, including blank lines, headings, and frontmatter. In this repository, the limit applies to every Markdown file, including skills, references, templates, README.md, and any requested plans. It is a hard requirement, enforced by sync validation and repository tests.

Condense wording and remove duplication before reaching the limit. Preserve accepted requirements and decisions. If necessary content cannot fit, pause and propose how to simplify the document or narrow the scope before proceeding. This limit does not require creating additional documents.
