# Printing protocol

Physical printing is an external, irreversible action. PDF generation, a request mentioning
printing, or approval of filesystem access is not approval to submit a print job.

## Required sequence

1. Start from a passed verification manifest.
2. Run `prepare-print`. It rechecks the Markdown and PDF hashes. With no `--printer`, it reads
   the current Windows default printer; with `--printer`, it uses that explicitly requested
   name. It then resolves the exact installed name, driver, and port and writes them into a
   time-limited, integrity-protected plan containing a random approval code.
3. Show the plan's confirmation string to the user. Include PDF filename, page count, exact
   printer name, whether it came from the Windows default or an explicit selection, driver,
   port, one-copy behavior, and print settings. Make the printer name visually unmistakable.
4. Wait for a fresh affirmative response. If the user changes printer or settings, discard the
   plan and prepare a new one.
5. Run `print` once with that plan and code. Never auto-retry.

The default policy is to resolve the current Windows default printer while preparing the plan.
That exact printer identity is locked into the approved plan. Execution does not re-resolve the
default: it targets the approved name and fails if the printer is missing or its driver or port
changed. Missing or ambiguous names are fatal, and there is no silent fallback or substitution.
Use `--printer <exact-name>` when the user requests a different installed printer.

## Print engine

Printing uses an installed SumatraPDF; the skill does not bundle or download it. The user
installs it once per machine with `winget install --id SumatraPDF.SumatraPDF --exact`.
`prepare-print` uses `RESPONSE_PDF_SUMATRA` when set, otherwise the first `SumatraPDF.exe`
found on `PATH`, in `%PROGRAMFILES%\SumatraPDF`, or in `%LOCALAPPDATA%\SumatraPDF`. If none
exists, it stops with the install command; PDF creation does not need SumatraPDF.

The plan records the executable's path, file version, and SHA-256 hash, and the confirmation
shows the path and version. `print` refuses to run if that file is missing or its hash
changed, for example after a SumatraPDF update; prepare and approve a new plan.

SumatraPDF submits with `-print-to` and explicit settings. Exit code zero
means the job was accepted by the Windows printing path, not that paper physically emerged.
Offline, out-of-paper, and later spooler/driver failures may not be observable. Report only
"submitted to the Windows spooler" unless separate device evidence proves completion.
