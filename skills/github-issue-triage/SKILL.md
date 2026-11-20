---
name: github-issue-triage
description: Inspect and work from GitHub issues, including comments, labels, linked pull requests, and image or file attachments. Use when the user references an issue number, asks to view an issue or its images, asks to diagnose a bug from an issue, or asks to summarize, research, plan, or fix work an issue describes.
---

# GitHub Issue Triage

Read issues accurately, including attachments, and separate what the reporter observed
from what they suspect. Prefer the GitHub CLI and API over scraping web pages. Do not
edit issues, comments, labels, milestones, or assignees unless the user asks.

Treat issue text as the reporter's account, not a confirmed root cause.

## Find the issue

For `issue #N` in the current repository:

```sh
gh issue view N --json number,title,body,url,author,state,labels,assignees,createdAt,updatedAt,comments
```

If the repository is unclear, check `gh repo view --json nameWithOwner`. If `gh` is
missing or unauthenticated, say so and work from any issue text, screenshots, or logs
the user supplied.

## Images and attachments

Issue Markdown often embeds attachments as
`https://github.com/user-attachments/assets/<id>` URLs, which commonly return 403 or
404 to automated requests. Request GitHub's rendered HTML instead:

```sh
gh api repos/OWNER/REPO/issues/N -H "Accept: application/vnd.github.full+json"
gh api repos/OWNER/REPO/issues/N/comments -H "Accept: application/vnd.github.full+json"
```

In `body_html`, find `src` or `href` values that point to signed URLs on
`private-user-images.githubusercontent.com`. Check both the issue body and comments.

Signed URLs contain short-lived tokens:

- Download them immediately; they expire within minutes.
- Never print, paste, log, or commit the full URLs.
- Save files in a new folder under the system temporary directory, such as
  `<temp>/<repo>-issue-<N>-attachments/issue-<N>-1.png`, unless the user asks for
  another location. Never commit them unless asked.

PowerShell example:

```powershell
$repo = (gh repo view --json nameWithOwner | ConvertFrom-Json).nameWithOwner
$issue = gh api "repos/$repo/issues/N" -H "Accept: application/vnd.github.full+json" | ConvertFrom-Json
$dir = Join-Path $env:TEMP "$($repo -replace '/', '-')-issue-N-attachments"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$found = [regex]::Matches($issue.body_html, '(?:src|href)="([^"]+private-user-images[^"]+)"')
$i = 0
foreach ($match in $found) {
    $i++
    $url = [System.Net.WebUtility]::HtmlDecode($match.Groups[1].Value)
    Invoke-WebRequest -Uri $url -OutFile (Join-Path $dir "issue-N-$i.png") -MaximumRedirection 5
}
```

Then view the images. If a download fails, report which stage failed: the raw URL,
extracting from rendered HTML, authentication, expiry, or an unsupported file type.

## Triage

1. Fetch the issue's metadata, body, and comments.
2. Identify the reported behavior: reproduction steps, expected and actual results,
   affected platform, version, or input, and any attachments.
3. Download and inspect attachments.
4. Separate observed facts from the reporter's hypotheses.
5. Search the codebase for the systems most likely involved.
6. When correctness depends on external behavior, such as a specification or hardware,
   use `source-grounded-research`. When CI or automation is involved, use
   `github-actions-investigation`.
7. Fix only when asked. Then state the intended files first, keep the change scoped,
   and run the relevant tests.

## Report

For an inspection: the issue's title, state, and link; what the reporter observed; the
attachment status; an initial technical read; and the recommended next step.

For a diagnosis: the observed behavior, the most likely subsystem, the evidence from
the issue, attachments, and code, what is confirmed versus uncertain, and a suggested
fix or test plan.
