# When to get agreement on a design change

These examples clarify the scope and design rule in INSTRUCTIONS.md.
They do not activate the optional plan-and-implement workflow.
If an agreed implementation outline sets stricter limits, follow those limits.

Get agreement on the new decision. Continue work that is already authorized
and does not depend on that decision.

## Example 1: Adding background retries while implementing Save

**Agreed task:** Add a Save button using the application's existing save API
and error handling.

**Discovery:** A save request can fail when the connection drops. The agent
considers introducing a service that stores failed requests and retries them
in the background.

**Decision requiring agreement:** Whether to introduce automatic retries.
This adds responsibilities for retaining requests, scheduling retries, and
handling duplicate saves.

The agent should explain:

> A failed save currently shows an error so the user can try again.
> Background retries would introduce new behavior and require decisions
> about retaining requests and preventing duplicate saves. I recommend
> following the existing error handling for this task and considering
> automatic retries separately.

The agent can continue implementing the button and existing error handling.
It must get agreement before adding the retry service.

## Example 2: Waiting for space in a firmware reply queue

**Agreed task:** Implement timed electrophoresis commands.

**Discovery:** When the outgoing queue fills, a reply can be rejected.
Some callers ignore that failure, so an acknowledgement can be lost even
though the command succeeded.

**Decision requiring agreement:** What should happen when the queue is full.
Waiting for transmission space preserves the reply but delays other work.
Handling the failure explicitly or increasing capacity has different costs.

The agent should explain:

> I found a queue-full case that can lose acknowledgements. One possible
> fix waits while earlier replies are transmitted, but that can postpone
> other firmware work, including servicing timed outputs. I recommend
> establishing the acceptable delay before choosing the queue-full policy.

The explanation must identify what waits, what work is postponed, and what
is known or unmeasured about the delay. A name such as makeRoomForPacket
does not explain those consequences.

The agent can investigate the failure and continue independent, agreed
work. It must get agreement before changing the queue-full behavior.

## Example 3: Correcting an agreed validation rule

**Agreed task:** Accept names containing up to 20 characters, including
exactly 20 characters.

**Discovery:** The existing check rejects names containing exactly 20
characters.

**Decision already authorized:** Correcting that boundary implements the
requested behavior within the existing validation function.

The agent should make the correction and verify the boundary cases.
It does not need separate agreement to choose a local variable name or
adjust the condition.

The agent should briefly mention the decision it made independently in its
change summary. For example:

> I changed the existing length check to accept exactly 20 characters
> because that matches the requested limit.

If the agent instead proposes replacing validation throughout the
application, that expands the scope and requires agreement first.
