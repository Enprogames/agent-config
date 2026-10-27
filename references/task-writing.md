# Writing useful tasks

Write brief, concrete tasks that someone can scan and act on without reading
this conversation. Use the examples below as guidance, not a mandatory template.

## Writing rules

- Name what fails and when, or what behavior needs to change.
- State the requested outcome and how someone can tell the task is complete.
- Use short paragraphs, meaningful labels, and bullets where they help scanning.
- Keep progress, build results, and investigation history in comments. Keep the
  description focused on the work and its completion checks.
- Replace vague claims such as "hardening," "improve robustness," "streamline,"
  or "seamless" with the specific failure and change. These words are not banned,
  but they do not explain the work on their own.
- Do not invent a root cause or claim verification that has not happened.
  Describe an uncertain cause as a hypothesis.
- Include only sections that help this task. A small task may need just a short
  problem statement and two or three completion checks.

## Example 1: Code signing after reboot

### Bad

**Title:** Harden code-signing workflow resilience

> Enhance authentication lifecycle management to improve pipeline robustness
> across machine state transitions. Implement appropriate hardening measures
> and validate operational readiness.

**Why it fails:** It hides the reboot trigger, password prompt, and required
outcome. "Hardening" adds no useful detail, and "operational readiness" does not
say what to verify.

### Good

**Title:** Fix unattended code signing after build-machine reboot

**Problem**
After the build machine reboots, SafeNet asks for the token password and blocks
unattended code signing.

**Done when**

- The first pipeline run after reboot signs the installer without manual token
  login.
- Missing signing secrets produce a clear error without exposing their values.
- The reboot-test result is recorded.

### Progress belongs in a comment

> PR #985 adds the secret mappings. Build #9455 passed. Verification after reboot
> is still pending.

This records what happened without making the task description a status log.
A passing build alone does not prove signing works after reboot.

## Example 2: Failed save

### Bad

**Title:** Improve save experience robustness

> Leverage enhanced error-handling capabilities to facilitate a seamless save
> journey and ensure appropriate user visibility into exceptional conditions.

**Why it fails:** It names no failure, required behavior, or observable result.

### Good

**Title:** Keep edits when saving fails

**Problem**
If saving fails, the editor clears the user's unsaved changes.

**Done when**

- A failed save leaves the edits visible and shows a clear error.
- The user can retry saving without re-entering their changes.

These checks describe the outcome without inventing a storage or retry design.
