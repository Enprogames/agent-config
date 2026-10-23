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

Discuss the simplest approach that meets the goal. Establish supported environments, important normal and failure behavior, and any compatibility, timing, cancellation, retry, or recovery rules relevant to this feature. Do not invent policies to cover hypothetical circumstances.

For each significant choice, record the decision, its reason and tradeoffs, its status, and the user's approval when given. Use Proposed, Approved, or Superseded. Explain meaningful alternatives when they help the user choose.

Ask about unresolved decisions in plain language, with a concrete example when useful. Obtain agreement before implementing behavior that depends on those choices.

## 3. Agree on the implementation outline

Present the implementation outline first as a compact, annotated hierarchy of files, classes, and functions, following the shared implementation-outline guidance. Attach additional execution explanations to the relevant parts.

Record the proposed changes to files, classes, and functions, including tests, documentation, and build wiring. For each relevant component or function, explain:

- Its name, responsibility, inputs, and results.
- Which functions call it and which functions it calls.
- The state it owns or changes and the relevant object lifetime.
- Important ordering, side effects, and failure behavior.
- Which approved requirement or decision justifies the change.

Justify new classes, helpers, modules, interfaces, and dependencies using a current need. Follow existing project terminology and patterns. A file-and-function list alone is not enough: walk through one normal operation and one important failure so the user can follow execution and state changes.

Agree on small implementation steps and review checkpoints. Obtain approval of the outline before coding. Existing explicit approval covers the decisions and steps it actually describes; a broad request to finish a feature does not approve unspecified design choices.

## 4. Implement the approved step

Change only the files and functions in the approved outline for the current step. Follow the agreed behavior, responsibilities, names, and call relationships. New helper functions and classes need outline entries unless the user explicitly delegated their introduction.

Routine local details, such as loop syntax and temporary variables, may be resolved within approved responsibilities. They must not introduce new behavior, ownership, dependencies, public interfaces, or structural changes.

At an agreed checkpoint, explain how the diff follows the plan, report verification actually performed, and wait for the agreed review before continuing. Do not request repeated approval for routine actions within an already approved step.

## When the design or outline needs revision

Pause the affected implementation before changing anything outside the approved outline or altering an approved decision. A failing test or newly discovered circumstance does not automatically authorize expanding the implementation.

Explain the current flow, what was discovered, and why the approved approach is insufficient. Give a short, educational explanation followed by this bullet-pointed summary:

- Discovery: the concrete behavior or constraint, with evidence.
- Impact: the requirement or approved approach that cannot be met as written.
- Recommended revision and tradeoffs: the smallest suitable change and meaningful alternatives.
- Approval needed: the exact decisions, files, functions, or steps to revise.

Record the proposal in the same document, clearly separated from the current approved specification and outline. Further investigation and drafting are allowed. Editing the document does not approve the proposal, and silence is not approval.

Wait for the user's agreement before implementing the revision. Then update the approved sections and mark replaced decisions Superseded. Revisiting the design is a normal, desired part of implementation.

## Verify and keep the document current

Use checks appropriate to the approved change. Preserve necessary safeguards. Inspect the diff for confusing control flow, unnecessary layers, speculative behavior, and changes outside the outline.

Walk through the implemented behavior using the agreed examples. Ensure the user can trace the change to its decisions and understand who owns each responsibility. Passing tests alone does not establish that the design is understandable.

Record actual progress, verification, limitations, and deferred improvements in the combined document. Give each deferred improvement a concrete future requirement or observed problem that would justify it; recording it does not authorize implementation.
