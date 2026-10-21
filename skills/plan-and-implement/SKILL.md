---
name: plan-and-implement
description: Plan and implement substantial software changes with a simple design and a living implementation plan. Use for new features or structural changes, not trivial edits.
---

# Plan and implement

Inspect the relevant code and project instructions. Reuse the project's terminology, existing patterns, and existing planning document when available.

Before implementation, explain:

- The requested behavior and what currently happens.
- The simplest suitable approach, including affected files and functions and how data moves through them.
- Any proposed new classes, interfaces, dependencies, or abstractions, and the current problem each solves.
- Important realistic failure cases and how the result will be checked.

Wait for the user's review of substantial structural decisions before coding. Treat an already accepted design as authorization to carry out its agreed steps without repeated approval requests.

Maintain one IMPLEMENTATION_PLAN.md alongside the code, unless the project already has an equivalent. Keep it brief and current:

- Agreed scope and observable completion criteria.
- Implementation approach and material decisions with their reasons.
- Progress, including verification actually performed.
- Deferred improvements and the specific condition that would justify each one.

Implement the agreed behavior with straightforward code. Record useful future improvements instead of building speculative infrastructure. Deferred improvements remain suggestions until authorized.

When new evidence materially changes the design, explain it and update the plan. Resolve routine details independently within the accepted scope. Finish by checking the diff for unnecessary complexity and reporting observed verification results.
