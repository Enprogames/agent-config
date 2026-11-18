---
name: compare-implementations
description: Compare independent implementations of a bounded software change. Explicit-only; use when the user requests or agrees to this workflow.
---

# Compare implementations

Use for bounded changes with meaningful design uncertainty and affordable validation.
If complete candidates are not feasible, agree on a narrower scope before starting.
Default to two candidates; use three only on request. Candidate work is proposal-only.
Follow shared and project requirements; applying a selected patch needs separate approval.
Do not invoke other explicit-only workflows unless requested.

1. Establish one brief: requirements, acceptance criteria, approved decisions,
   exclusions, applicable instructions, and common checks. Record the starting
   commit and an exact snapshot of current working files, including relevant
   uncommitted and untracked content. Give every candidate the same brief and baseline.
   Reconcile conflicting sources with current approved decisions; resolve outstanding
   contract or policy choices with the user before dependent implementation.
2. Create an owned detached temporary worktree for each candidate and populate it
   from that baseline. Leave the original working files, branch, and index untouched.
   Check the shared build/test setup on the baseline before spawning candidates;
   keep discovery and execution from modifying the user's configuration.
   Spawn fresh agents concurrently without the orchestrator's conversation history.
   Assign each its worktree's absolute path; require explicit working directories
   for commands and absolute paths for edits. If delegation or isolation is
   unavailable, report the limitation instead of silently substituting another workflow.
3. Each agent reads applicable instructions, investigates existing ownership,
   callers, contracts, and comparable implementations, then implements and verifies
   within the brief. Candidates may converge; do not force artificial differences.
   Workers hand off provisional candidates and do not delegate further agents.
4. Use the same acceptance and regression checks for all candidates; assess added
   tests against the requirements. Worktrees share machine resources: isolate
   conflicting outputs or serialize checks. After workers finish, obtain one fresh
   independent `review-code` review of the viable candidates and wait for findings.
   Follow its handoff, findings, and recheck procedure.
5. Compare while the worktrees remain available. Unmet requirements disqualify a
   candidate. Explain tradeoffs in existing-pattern fit, responsibility boundaries,
   interface and caller clarity, information hiding, failure handling, and review
   effort. Prefer the smallest cohesive solution, not the fewest changed lines.
   Treat a combined implementation as a new candidate requiring validation and review.
6. Save the baseline, complete candidate patches against it (including new files),
   check results, and limitations outside the worktrees. Verify the exports can
   reconstruct the validated candidates. Once workers and candidate processes stop,
   remove only owned worktrees through Git. Preserve unexpected edits and report
   cleanup limitations.
   Use retained artifact paths in reports so links survive cleanup.
7. Recommend one candidate and at most one worthwhile alternative; say when none
   qualifies or candidates are equivalent. Present concrete tradeoffs, complete
   diffs, and verification results. Obtain approval before applying a selected patch
   to the original working tree.
