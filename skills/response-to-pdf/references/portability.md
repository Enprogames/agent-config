# Host portability

The source of this skill is the `agent-config` repository. Its `sync.py` installs a copy in
each selected agent's global skills directory; edit the repository source, not an installed
copy.

## Exact preceding-response capture

Codex Desktop and CLI normally expose `CODEX_THREAD_ID` to subprocesses. `capture-codex` starts
the local Codex App Server, reads only that thread, selects its most recent stored
`agentMessage` whose phase is `final_answer`, and writes the returned text bytes directly.

Other hosts do not share a standard current-message API. If a host supplies an equivalent
trusted transcript tool, use its exact message record. Otherwise the agent must not claim
byte-for-byte capture: ask the user to paste/attach the content or approve a context-derived
Markdown source before rendering.

PDF rendering from an already supplied Markdown file remains deterministic across hosts that
have Python 3.14, `uv`, a Chromium browser, and Poppler. Physical printing is Windows-only and
requires access to the local printer subsystem and an installed SumatraPDF.
