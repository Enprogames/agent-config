This repository maintains shared instructions and skills for Ethan's coding agents.

Read INSTRUCTIONS.md for the user's preferences. Keep the sync implementation as straightforward functions using the Python standard library. Preserve unrelated agent configuration and locally edited installed files.

Every Markdown document in this repository must contain at most 300 lines, counting blank lines, headings, and frontmatter. This includes instructions, skills, references, templates, README.md, and any requested plans. Do not weaken the limit or bypass its checks.

The plan-and-implement workflow is explicit-only. Creating, editing, or reviewing a skill does not invoke the skill being edited. Do not create a planning or status document for this repository unless the user requests one or explicitly chooses that workflow.

Run `python verify.py` and `python -m unittest discover -s tests -v` after any repository change, including documentation edits. Verification checks UTF-8 without a BOM, LF endings, a final newline for nonempty text files, and document lengths. Sync uses the same checks before installation. GitHub checks run both commands on pushes and pull requests.

Exercise installation only against a temporary home directory during development. Installing into the real user's configuration is a separate, explicit action.

Keep platform paths and usage examples in README.md consistent with sync.py.
