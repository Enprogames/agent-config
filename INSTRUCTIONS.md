# Shared agent instructions

## General preferences

- Communicate plainly and concretely. State exactly what you mean, use specific details, and define necessary terms. Be concise. Include brief examples when they prevent ambiguity, and code snippets or diagrams only when they clarify better than prose alone.
- Write task titles and descriptions in plain, concrete language. State the problem, requested outcome, and observable completion checks. Keep progress updates in comments. Follow [task-writing examples](references/task-writing.md).
- Begin implementation descriptions with a compact, annotated hierarchy of the relevant files, classes, and functions. Show each element's purpose and important behavior beside it. Follow [implementation outline guidance](references/implementation-outlines.md), and expand execution details when the hierarchy alone is insufficient.
- Write code the user can understand, debug, and maintain.
- Follow existing terminology and patterns. Prefer straightforward functions and control flow; justify new abstractions with a current need.
- Implement the smallest cohesive change that fully satisfies the request and fits the existing architecture. Consider implementation clarity and review effort. Include necessary tests and documentation; do not weaken correctness or duplicate feature logic merely to reduce the diff.
- Include supporting refactors only for a concrete need in the current change. Before substantial implementation, identify them and explain that need. Small local improvements that clarify the changed behavior are permitted; “improves maintainability” alone does not justify broader restructuring.
- Flag independent bugs, cleanup, modernization, or hardening with their impact and a suggested follow-up. Do not implement them or create tickets without authorization. Get agreement before substantially expanding scope or changing an agreed design; continue independent, agreed work. Consult [scope and design examples](references/design-agreement-examples.md) when the boundary is unclear.
- Verify relevant behavior and review the final diff against the agreed scope. Remove agent-introduced incidental churn; preserve existing encoding, line endings, and unrelated user changes. Report actual changes, checks, and remaining limitations.

## Skills

Detailed procedures belong in each skill's SKILL.md, rather than this document.

Skills marked explicit-only require the user's request or agreement before starting their workflow or creating their documents. You may recommend them.

Creating, editing, or reviewing a skill does not invoke that skill.

- `plan-and-implement` — **Explicit-only:** agree on a feature's specification, design decisions, and implementation outline in one document, then implement approved steps with review checkpoints.
- `review-code` — Review a requested software change for concrete bugs, unmet requirements, and unnecessary complexity, separating defects from optional improvements.

## Maintenance

Maintain shared instructions and skills in `agent-config`, rather than installed copies. Keep project-specific guidance with the project.

Instruction documents must not exceed 300 lines, including blank lines, headings, and frontmatter.
