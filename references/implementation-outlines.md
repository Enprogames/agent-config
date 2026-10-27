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

In proposed or mixed outlines, label changed entries [new], [modify], or
[remove], and unchanged dependencies [context]. When every entry describes
existing code, label the explanation "Existing implementation explanation
— [area]" and omit per-item status labels and emojis. Keep the annotated
hierarchy and behavioral details.
Use actual names for existing code and clearly identify proposed new names.

In a formal implementation outline, include all planned changes, including
tests, documentation, and build wiring. In an explanation of existing code,
include only the parts relevant to the question.

## Styling

Render the hierarchy as nested Markdown lists outside fenced code blocks.
Use bold inline-code names for files, classes, and functions. Keep explanations
in normal text, with bold annotation labels such as Calls, Success, and Failure.

For proposed or mixed outlines, use consistent status cues: 🟢 **[new]**, 🟡 **[modify]**, 🔴 **[remove]**,
and ⚪ **[context]**. When using status cues, retain their text labels; color is supplementary.
Use standard Markdown rather than renderer-specific HTML/CSS or ANSI colors.

## Annotations

Give each entry a short, concrete purpose or description of its change.
Add relevant details beside the entry:

- Inputs and results.
- Which functions call it and which functions it calls.
- State ownership and changes, including object lifetime when relevant.
- Important ordering, side effects, and failure behavior.

Explain shared responsibilities once, beside their owner. Use short phrases
and omit empty or irrelevant fields. Keep meaningful names consistent
throughout the explanation.

Prefer concrete descriptions such as "preserves the draft and displays
SaveError" over broad phrases such as "handles failures."

## Examples

### Proposed change

Illustrative example:

- **`src/DocumentEditor.ts`** · 🟡 **[modify]**

  - **`DocumentEditor`** · 🟡 **[modify]** — owns `draft` and `saveStatus` for this editor's lifetime.

    - **`save()`** · 🟢 **[new]** — submit a snapshot of the current draft.

      - **Calls:** `await saveDocument(snapshot)`.
      - **Success:** `saveStatus = saved`.
      - **Failure:** keep draft; `saveStatus = error`; display `SaveError`.

- **`src/DocumentApi.ts`** · ⚪ **[context]**

  - **`saveDocument(snapshot) → saved revision`** — sends one request; rejects with `SaveError`; no automatic retries.

### Existing implementation explanation — document saving

Illustrative example.

- **`src/DocumentEditor.ts`** — editor state and save action.

  - **`DocumentEditor`** — owns `draft` and `saveStatus` for the editor's lifetime.

    - **`save()`** — captures the current draft and awaits `saveDocument(snapshot)`.

      - **Success:** sets `saveStatus = saved`.
      - **Failure:** preserves the draft, sets `saveStatus = error`, and displays `SaveError`.

- **`src/DocumentApi.ts`** — persistence request.

  - **`saveDocument(snapshot) → saved revision`** — sends one request; rejects with `SaveError`; does not retry automatically.

## Execution details

The tree shows containment, not execution order.

Make waiting, deferred work, callbacks, and consequential state changes
explicit whenever they affect understanding. A label such as "process"
or "make room" does not explain those effects.

For formal implementation plans, walk through one normal operation and one
important failure. For other explanations, add a walkthrough, sequence diagram,
state model, or worked example only when the annotations do not explain the
execution clearly. Place these details immediately after the relevant tree.

Start with the hierarchy, then expand the difficult parts. Do not repeat
the same information in several formats.
