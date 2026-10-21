This repository maintains shared instructions and skills for Ethan's coding agents.

Read INSTRUCTIONS.md for the user's preferences. Keep the sync implementation as straightforward functions using the Python standard library. Preserve unrelated agent configuration and locally edited installed files.

Run `python -m unittest discover -s tests -v` after changing sync.py. Exercise installation only against a temporary home directory during development. Installing into the real user's configuration is a separate, explicit action.

Update IMPLEMENTATION_PLAN.md when the setup status or agreed scope changes. Keep platform paths and usage examples in README.md consistent with sync.py.
