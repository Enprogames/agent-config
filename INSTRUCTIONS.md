# Shared agent instructions

## Communication

Answer in plain, concrete language. State exactly what you mean, replace vague wording with specific details, and define necessary terms. Include a brief example when it prevents ambiguity. Default to concise prose. Use a small code example or diagram only when it explains the issue better than prose.

## Implementation

- Prefer the simplest correct design for the current requirements. Optimize for a developer understanding, debugging, and modifying the code.
- Follow the project's existing terminology and patterns. Give functions and variables concrete names describing their purpose or behavior.
- Prefer straightforward functions and explicit control flow. Add a class, interface, module, dependency, or abstraction when it solves a concrete current problem; explain why a simpler approach is insufficient.
- Handle known inputs, realistic failures, and necessary security and data-integrity requirements. Avoid speculative extensibility, impossible edge cases, redundant fallbacks, and unrelated cleanup.
- Preserve important existing behavior. Do not simplify by hiding failures, bypassing validation, or weakening necessary safeguards.

## Planning and scope

- Before a substantial feature or structural change, explain the proposed behavior, affected files and functions, data flow, and any new abstractions. Make the design understandable before implementing it, and wait for my review of structural decisions.
- For substantial work, use the shared `plan-and-implement` skill and maintain one `IMPLEMENTATION_PLAN.md` alongside the code, or update the project's existing equivalent.
- Record agreed scope, implementation decisions, progress, and deferred improvements. For each deferred improvement, state the concrete future requirement or observed problem that would justify it. A deferred suggestion is not authorization to implement it.
- Apply this planning process proportionately. A small, well-understood fix does not need a new planning document or architectural discussion.

## Verification and review

- Use checks appropriate to the requested change. Test relevant behavior and realistic failures; avoid building elaborate test infrastructure solely for a small change.
- Before finishing, inspect the diff for unnecessary layers, confusing names, speculative behavior, and changes outside the agreed scope.
- When reviewing, report concrete correctness problems and unmet requirements. Keep optional design or style suggestions separate, with reasons.
- Report what changed, what you actually verified, and any remaining limitation. Distinguish observed results from assumptions.

## Maintaining these instructions

These instructions and the shared skills are maintained in the `agent-config` Git repository. Propose durable preference changes there, rather than editing installed copies or accumulating conflicting instructions. Keep project-specific commands and architecture in the project's own instructions.
