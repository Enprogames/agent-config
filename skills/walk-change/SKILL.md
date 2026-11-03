---
name: walk-change
description: Explain a software change interactively and propose justified ways to reduce its scope or complexity. Explicit-only; use when the user invokes walk-change or agrees to use this workflow.
---

# Walk through a change

Use only when explicitly requested or agreed. Explain and recommend; apply changes
only when the user requests them.

1. Establish the requested comparison and story goal from available context.
   Identify acceptance criteria and exclusions, and distinguish a disposable PoC
   from a change intended to merge. Keep committed, staged, and unstaged changes
   distinct where relevant; ask about missing context only when it affects the advice.
2. Inspect the diff and relevant surrounding code. Begin with a compact annotated
   hierarchy of files, classes, and functions, then trace the important execution
   flow and failure behavior. Explain what each changed component contributes.
3. Walk through coherent portions, pausing for questions before continuing unless
   the user requests the complete walkthrough at once.
4. For each useful cut, identify its location, what it enables, the specific removal
   or simpler alternative, dependencies, and consequences. Separate necessary fixes,
   optional simplifications, and independent follow-ups.
5. Keep behavior, tests, and supporting changes needed for the story. Defer unrelated
   cleanup and longstanding bugs, but explain when the story exposes or depends on
   fixing an existing bug. Name any consequences of PoC shortcuts for a mergeable PR;
   get agreement before changing accepted requirements.
6. Reduce unnecessary scope and complexity rather than chasing line count.
   Do not invent cuts; say when no useful cuts remain.
