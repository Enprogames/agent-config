---
name: plan-and-implement
description: Run the user's design-and-implementation workflow only when they explicitly request plan-and-implement or agree to use it. Agree on a feature's specification, decisions, and implementation outline, then implement approved steps with review checkpoints.
---

# Plan and implement

Help the user create code they understand and can maintain. Significant behavior and structure must follow agreed decisions; completing the task quickly does not justify making those decisions silently.

## Explicit activation only

Use this workflow only when the user explicitly requests it or agrees to a recommendation to use it. You may recommend it, but wait for agreement before starting the workflow or creating its planning document. Ordinary implementation requests and preferences for understandable code are not invocation.

Creating, editing, or reviewing this skill does not invoke it. Treat its contents as material being authored or reviewed in those tasks; do not apply its process to the authoring task unless the user separately requests that.

Once explicitly chosen for a feature, continue the workflow through its approved steps and review checkpoints without requiring the user to invoke it again on every message. Stop using it when the user ends or replaces that workflow.

## One combined document

Maintain one feature document with the code and branch: IMPLEMENTATION_PLAN.md, or the project's existing equivalent. Keep the goal, specification, design decision register, implementation outline, proposed revisions, progress, verification, and deferred improvements together.

Read [assets/IMPLEMENTATION_PLAN.md](assets/IMPLEMENTATION_PLAN.md) when creating a plan. Adapt that template to the feature; do not create separate specification or decision-register documents.

Every instruction document, including this skill and the combined plan, must be at most 300 lines, counting blank lines, headings, and frontmatter. Condense wording and duplication without silently discarding accepted requirements or decisions. If essential content cannot fit, pause and propose a simpler document or narrower scope. Do not split the combined plan to bypass the limit.

## 1. Confirm the goal and investigate

Restate the requested outcome, observable acceptance criteria, and exclusions. An unambiguous user request may already establish these; do not ask for redundant confirmation.

Inspect the relevant existing code and project instructions before proposing a design. Explain the current behavior, conventions, dependencies, and ownership that matter. Distinguish observed facts from assumptions and unresolved questions. Investigation is read-only unless an experiment is separately authorized.

## 2. Agree on behavior and design decisions

Apply the shared advice-and-decisions agreement while comparing approaches. Establish the required normal and failure behavior, supported environments, and relevant compatibility, timing, retry, recovery, or cancellation rules. Explain meaningful alternatives; do not invent policies for hypothetical circumstances.

Record each significant choice, its basis and tradeoffs (including important assumptions and accepted downsides), status, and approval reference. Use Proposed, Approved, or Superseded. Add a reconsideration trigger only when there is a concrete one.

Record explicit user choices as Approved and proposals as Proposed. Preserve unrelated implementation approvals and review checkpoints. Resolve open choices before implementing behavior that depends on them.

## 3. Agree on the implementation outline

Before drafting the outline, read the implementation-outline guide referenced by the shared instructions. Link each planned change to its acceptance criteria or approved decisions, and justify new abstractions or dependencies with a current need.

Agree on small implementation steps and review checkpoints. Obtain approval of the outline before coding. Existing explicit approval covers the decisions and steps it actually describes; a broad request to finish a feature does not approve unspecified design choices.

## 4. Implement the approved step

Read the current approved decisions and outline. Implement the current step within its listed files, functions, behavior, and responsibilities. New helper functions and classes need outline entries unless the user explicitly delegated their introduction.

Routine local details, such as loop syntax and temporary variables, may be resolved within approved responsibilities. They must not introduce new behavior, ownership, dependencies, public interfaces, or structural changes.

At an agreed checkpoint, explain how the diff follows the plan, report verification actually performed, and wait for the agreed review before continuing. Do not request repeated approval for routine actions within an already approved step.

## When the design or outline needs revision

Apply the shared agreement's reconsideration and pause boundaries. Continue unaffected approved work; do not apply the proposed revision until the user chooses it. Diagnose failing tests before assuming the design must change; fix within the approved scope when possible.

Explain the discovery with evidence, affected decision and impact (including whether work is blocked), recommended revision and tradeoffs, and exact approval needed. Present each point once, using the clearest format. Add a walkthrough only when needed to explain execution.

Record the proposal separately from the current approved specification and outline. Investigation and drafting do not authorize implementation of the revision, and silence is not approval.

After the user selects a revision, update the affected specification and outline, record approval, and mark replaced decisions Superseded.

## Verify and keep the document current

Use checks appropriate to the approved change. Preserve necessary safeguards. Inspect the diff for confusing control flow, unnecessary layers, speculative behavior, and changes outside the outline.

Walk through the implemented behavior using the agreed examples. Ensure the user can trace the change to its decisions and understand who owns each responsibility. Passing tests alone does not establish that the design is understandable.

Record actual progress, verification, limitations, and deferred improvements in the combined document. Give each deferred improvement a concrete future requirement or observed problem that would justify it; recording it does not authorize implementation.
