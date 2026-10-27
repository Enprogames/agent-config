# Document review examples

These excerpts and paths are illustrative, not findings about this repository.
They calibrate judgment; do not use them as a required report template.

## Conflicting copies of a rule

**Material:** `INSTRUCTIONS.md` says deployment requires approval, with a named
exception for a test environment. `release.md` repeats the rule but omits that
exception and does not identify the source policy.

**Useful finding:** The two copies give different answers for test deployments.
Keep the policy and exception in the owning document. In `release.md`, point to
that policy and retain only the reminder needed at the deployment step.

**Poor finding:** "Consolidate governance for improved instruction cohesion."
This names neither the disagreement nor a correction that preserves the rule.

## Vague task wording

**Material:** A task says "Harden signing resilience across machine state
transitions" without naming the failure or success condition.

**Useful finding:** The title hides that signing asks for a password after
reboot. Name that trigger and specify whether the first signing run must finish
without manual login. Do not claim the cause or fix is proven.

For full good/bad task descriptions, use the task-writing guide linked from the
shared instructions instead of copying it into this skill.

## A reminder that is not harmful duplication

**Material:** An overview defines approval requirements. A command example
briefly reminds the reader to obtain that approval before deleting data and
links back to the policy.

**Judgment:** Keep the reminder. It is useful at the point of action and does
not maintain a second policy. Repeated words alone do not establish bloat.

## A shorter rewrite that loses requirements

**Material:** "Retry at most three times with the same idempotency key. Stop on
a permanent authentication error."

**Poor correction:** "Retry failed requests."

**Judgment:** Reject that cut. It removes the retry bound, duplicate-prevention
requirement, and stopping condition. A useful rewrite must preserve all three;
word-count reduction alone is not an improvement.

## Distribution does not prove loading

**Material:** The inspected sync code copies `references/signing.md`. The guide
is intended to be read before signing, but the scoped instructions contain no
reference to it. The live installed configuration has not been inspected.

**Useful finding:** The source is configured for distribution, but the required
reading has no route from the stated entry point. Add a reference where signing
work is introduced, naming when to read the guide. Installation and loading
remain unverified.

**Poor finding:** "The agent ignores this guide."
That conclusion needs behavioral evidence. If a reference is intentionally
optional or supplied directly with a task, do not demand a global instruction
that loads it for unrelated work.

## Essential information available only in an image

**Material:** A setup guide contains an unlabeled screenshot showing the only
copy of a required setting and its value.

**Useful finding:** A reader who cannot inspect the image cannot complete the
step. Put the setting name and value in the step text and use the screenshot as
support. Do not claim the whole document meets an accessibility standard from
this check alone.

## No material findings

**Material:** A short guide has a clear purpose, consistent rules, working
references, and examples that explain its only difficult case.

**Useful result:** "No material findings in the requested guide. Installation
and runtime loading were outside the review scope."

Do not add cosmetic rewrites merely to make the report look productive.
