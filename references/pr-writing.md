# Writing PR titles and summaries

Follow the repository's PR instructions and template. Apply this style to its
summary or equivalent section, preserving required title conventions, sections,
and checklists. Without additional description requirements, use the summary
alone as the PR description.

## Titles

Name the main change and affected behavior or component, using a concrete action
such as Fix, Keep, Add, or Remove. Replace vague claims with the specific change.

| Vague | Concrete |
| --- | --- |
| Improve logging | Restore global logging after command-line setup |
| Harden save handling | Keep unsaved edits when saving fails |
| Refactor command code | Share packet encoding between timed commands |

## Summaries

- Start with two or three sentences explaining the problem, resulting behavior,
  and reason for the change.
- Follow with bullets for meaningful groups of changes. Usually use two short
  sentences per bullet: what changed, then its purpose or effect.
- Include material test, documentation, and configuration changes where relevant.
  Use technical names only when they help the reviewer.
- Describe the final change and support claims with the diff and actual
  verification. Keep simple PRs shorter; do not pad to meet sentence counts.

## Illustrative example

**Title:** Keep unsaved edits when saving fails

When saving fails, the editor currently clears the user's unsaved changes.
This change preserves those edits and displays an error so the user can retry.

- **Preserve failed saves.** The editor now clears its unsaved state only after
  a successful save. A failed request leaves the entered text available for
  another attempt.
- **Explain the failure.** The editor displays the existing save error message
  when a request fails. The Save button remains available for a manual retry.
- **Cover save and retry behavior.** Tests check that failed saves retain the
  draft and successful saves clear the unsaved state. They also cover successfully
  saving the retained draft on a later attempt.
