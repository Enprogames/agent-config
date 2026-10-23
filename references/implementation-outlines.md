# Compact implementation outlines

Begin an implementation explanation with an annotated tree. Give the reader
a quick structural overview containing enough behavior to understand what
each part does.

Use this format in chat and in implementation plans. It does not require
creating a planning document or activating the plan-and-implement skill.

## Structure

Arrange entries by containment:

- File
  - Class, when applicable
    - Function or method

Place module-level functions directly beneath their file. Include relevant
state beside the component that owns it.

For proposed changes, label entries [new], [modify], or [remove].
Label unchanged dependencies included for explanation [context].
Use actual names for existing code and clearly identify proposed new names.

In a formal implementation outline, include all planned changes, including
tests, documentation, and build wiring. In an explanation of existing code,
include only the parts relevant to the question.

## Annotations

Give each entry a short, concrete purpose or description of its change.
Add relevant details beside the entry:

- Inputs and results.
- Important functions it calls.
- State it owns or changes, including its lifetime when relevant.
- Important side effects and failure behavior.

Explain shared responsibilities once, beside their owner. Use short phrases
and omit empty or irrelevant fields. Keep meaningful names consistent
throughout the explanation.

Prefer concrete descriptions such as "preserves the draft and displays
SaveError" over broad phrases such as "handles failures."

## Example

Illustrative proposed change:

```text
src/DocumentEditor.ts [modify]
└─ DocumentEditor [modify]
   Owns: draft and saveStatus for this editor's lifetime.
   └─ save() [new] — submit a snapshot of the current draft
      Calls: await saveDocument(snapshot).
      Success: saveStatus = saved.
      Failure: keep draft; saveStatus = error; display SaveError.

src/DocumentApi.ts [context]
└─ saveDocument(snapshot) → saved revision
   Sends one request; rejects with SaveError; no automatic retries.
```

## Execution details

The tree shows containment, not execution order.

Make waiting, deferred work, callbacks, and consequential state changes
explicit whenever they affect understanding. A label such as "process"
or "make room" does not explain those effects.

When the annotations cannot explain the execution clearly, add a short
numbered walkthrough, sequence diagram, state model, or worked example
immediately after the relevant tree.

Start with the hierarchy, then expand the difficult parts. Do not repeat
the same information in several formats.
