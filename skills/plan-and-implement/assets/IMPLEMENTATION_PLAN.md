# Feature implementation plan

Status: Proposed. Implementation has not been approved.
Specification approval: Pending.
Implementation outline approval: Pending.

Keep this document at or below 300 lines, including blank lines and headings. Replace the prompts below with feature-specific content. Keep the specification, decision register, and implementation outline together.

## Goal and acceptance criteria

- User story: [Who needs what outcome, and why?]
- Acceptance criteria: [Observable examples that establish completion.]
- Exclusions: [Behavior and improvements outside this feature.]

## Existing behavior and specification

- Current implementation: [Relevant existing flow, conventions, and constraints.]
- Required behavior: [Inputs, outputs, supported environments, and examples.]
- Important failure behavior: [Agreed outcomes and side effects for realistic failures.]
- Open questions: [Unresolved facts or decisions; do not silently assume answers.]

## Design decision register

Use Proposed, Approved, or Superseded. Record approval only when the user gives it.

| ID | Status | Decision | Reason and tradeoffs | Approval reference |
| --- | --- | --- | --- | --- |
| D1 | Proposed | [Specific choice.] | [Current need and consequences.] | Pending |

## Implementation outline

Begin with an annotated tree following the shared implementation-outline guidance. Include code, tests, documentation, and build wiring. Explain inputs and results, call relationships, state ownership, object lifetime, and important failure behavior where relevant. Link entries to their acceptance criteria or approved decisions. Walk through one normal operation and one important failure.

```text
[file path] [new/modify/remove]
└─ [class, when applicable]
   └─ [function] — [purpose and planned change]
      [Relevant inputs/results, calls, state, effects, or failures.]
```

Allowed local details: loop syntax and temporary variables within approved responsibilities. New helpers, classes, or changes outside this outline require approval unless explicitly delegated.

## Implementation steps and review checkpoints

- [ ] Step 1: [Bounded change and its checks.] Review checkpoint: [When the user reviews before further work.]

## Proposed revisions

None. When needed, record the discovery, impact, recommended revision and tradeoffs, and exact approval needed here. Preserve the current approved sections until the user agrees; then integrate the revision and update decision statuses.

## Progress and verification

Not started. Record work actually completed, checks actually run, observed results, and remaining limitations.

## Deferred improvements

None. Give each suggestion a concrete future requirement or observed problem that would justify it. Suggestions are not approved implementation work.
