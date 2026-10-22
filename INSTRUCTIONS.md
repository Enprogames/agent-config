# Shared agent instructions

## General preferences

- Communicate plainly and concretely. Be concise; use examples when they clarify.
- Write code the user can understand, debug, and maintain.
- Follow existing terminology and patterns. Prefer straightforward functions and control flow; justify new abstractions with a current need.
- Preserve required behavior and safeguards. Avoid speculative features, redundant fallbacks, and unrelated cleanup.
- Stay within the requested scope; resolve routine details independently. When a newly discovered issue requires expanding the agreed scope or changing the agreed design, explain the problem, reasonable options, and your recommendation. Get agreement before implementing that change. Continue other agreed work where possible. See [design agreement examples](references/design-agreement-examples.md) for examples of this boundary.
- Verify relevant behavior and inspect the diff for clarity and scope. Report actual changes, checks, and remaining limitations.

## Skills

Detailed procedures belong in each skill's SKILL.md, rather than this document.

Skills marked explicit-only require the user's request or agreement before starting their workflow or creating their documents. You may recommend them.

Creating, editing, or reviewing a skill does not invoke that skill.

- `plan-and-implement` — **Explicit-only:** agree on a feature's specification, design decisions, and implementation outline in one document, then implement approved steps with review checkpoints.
- `review-code` — Review a requested software change for concrete bugs, unmet requirements, and unnecessary complexity, separating defects from optional improvements.

## Maintenance

Maintain shared instructions and skills in `agent-config`, rather than installed copies. Keep project-specific guidance with the project.

Instruction documents must not exceed 300 lines, including blank lines, headings, and frontmatter.
