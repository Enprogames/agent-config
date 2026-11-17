---
name: review-code
description: Review a software change for concrete bugs, unmet requirements, and unnecessary complexity. Use when the user requests a code review.
---

# Review code

Read the requested diff and the surrounding code needed to understand it. Establish the intended behavior from the task, project instructions, and implementation plan when available.

Prioritize concrete correctness problems, regressions, necessary security and data-integrity issues, and unmet requirements. Explain how each issue occurs and point to the relevant code. Verify an assumption when practical before treating it as a finding.

Check added guards, early returns, fallbacks, and wrappers for changed contracts. Verify test expectations against the requirement, not merely the new implementation.

Also identify complexity that makes the change materially harder to understand: unnecessary indirection, unclear names, speculative abstractions, redundant branches, or unrelated changes. Explain the specific simpler alternative and its tradeoff. Do not impose a different architecture merely because you prefer it.

Review the change as a maintainer unfamiliar with this chat. Check whether its purpose, owning component, important state transitions, and failure paths are clear. Keep behavior changes distinguishable from behavior-preserving refactoring, and include enough caller context to show new interfaces in use.

Keep optional improvements separate from defects. Describe the future requirement or observed problem that would justify an optional improvement. Do not create implementation work from hypothetical edge cases or treat every review suggestion as mandatory.

Report no findings when the evidence supports that result. State any important review limitation. When reviewing a change you wrote in the same session, state that as a limitation and recommend an independent review for substantial changes. A review request alone does not authorize rewriting the code.
