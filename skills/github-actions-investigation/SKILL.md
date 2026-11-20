---
name: github-actions-investigation
description: Diagnose or fix GitHub Actions failures, including CI, pull request, scheduled, dependency update, coverage, audit, artifact, and release workflows, or a saved CI log. Use when the user asks why a workflow failed, asks to inspect a specific run or log file, asks about the latest failure, or asks to fix a pipeline.
---

# GitHub Actions Investigation

Find the workflow, job, and step that actually failed, separate the root cause from
later noise, and either explain it or make the smallest durable fix.

## Choose the mode

- **Diagnose:** inspect evidence, explain the root cause, and recommend a concrete fix.
  Do not edit files.
- **Fix:** diagnose first, state the intended fix and the files it touches, edit them,
  and run targeted verification.

When the request is ambiguous, diagnose.

## Find the run

1. **Saved log file:** inspect the named file first. Search for high-signal lines such as
   `::error::`, `error:`, `failed`, `FAIL`, `panicked`, `exit code`, `not found`,
   `deprecated`, `permission`, `unauthorized`, `No such file`, and `locked`.
2. **Specific run:** accept a run URL, run ID, workflow name, job name, branch, or SHA.
   Take the numeric ID from `/actions/runs/<id>` in a URL.
3. **Latest run:** `gh run list --limit 1`, then inspect that run.
4. **Latest run for the current pull request:**
   - `gh pr view --json number,headRefName,headRefOid,url`
   - `gh run list --branch <headRefName> --limit 20`
   - Prefer `pull_request` runs whose head SHA matches the pull request's head SHA.
     If none matches exactly, say which run you chose instead.

If `gh` is unavailable or unauthenticated, or the branch has no pull request, fall back
to local logs and workflow files and say what was missing.

## Collect evidence

Start with read-only commands:

```sh
gh run view <run-id> --json status,conclusion,workflowName,event,headBranch,headSha,jobs
gh run view <run-id> --log-failed
```

Then read the files that define the failing behavior:

- `.github/workflows/*.yml` and `*.yaml`
- local actions under `.github/actions/`
- `.github/dependabot.yml` when dependency updates are involved
- the project's manifests, lockfiles, and toolchain files used by the failing step

The last visible error is often not the cause. Find the earliest failing command in the
failed job, and describe cascading failures separately.

## Classify the failure

Name one or more categories:

- project code or test failure
- dependency or lockfile failure
- language toolchain failure
- missing native or operating system dependency
- workflow syntax or configuration error
- action version, runtime, or deprecation problem
- permissions, token, or secret problem
- cache or tool installation failure
- artifact upload or download failure
- external service failure, such as a coverage service
- scheduled maintenance check, such as a security audit or outdated dependency check
- runner or network flake

Verify changeable facts, such as current action versions, hosted runner images, or
runtime deprecations, against official documentation before recommending a change.

## Reproduce locally

Map the failed step to the smallest local command that exercises the same behavior.
Take commands from the workflow file and the repository's instructions rather than
guessing. Run the same flags where they matter, such as locked dependency resolution.
Say which steps cannot be reproduced locally, such as those needing secrets, other
operating systems, or external services.

## Fixing

- Prefer the smallest durable fix over hiding the symptom.
- Keep workflow changes deterministic. Pin tool versions where reproducibility matters.
- Do not weaken or skip a check unless the user accepts that tradeoff.
- Do not make correctness depend on stale cache contents.
- Run the narrowest relevant local check, then broader checks if the fix affects shared
  workflow behavior.

## Report

For a diagnosis, give:

- the failed workflow, job, and step;
- the root cause, with the decisive log line or command;
- its category from the list above;
- a specific recommended fix.

For a fix, give the changed files, the verification commands and results, and any
validation that can only happen in the pipeline.
