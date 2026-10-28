# Building C++/CLI and .NET projects

Read the repository's build instructions before choosing commands. These rules
apply when .NET code has C++/CLI or native dependencies, including through
project references. Keep project-specific commands and test exclusions in that
project's documentation and link them from its agent guide.

## Inspect the requirements

Check target frameworks, CLR mode, C++ toolset, configuration, platform
mappings, and native dependencies. Distinguish .NET Framework from modern .NET;
their C++/CLI requirements differ. An SDK-style C# project can still reference
legacy or native projects, and an Any CPU mapping can still produce x86 code.

Discover an installed Visual Studio toolchain compatible with the project,
using Developer PowerShell or `vswhere`. Check for C++/CLI support and required
SDKs/targeting packs. Do not assume an edition, installation path, or that the
.NET SDK supplies the C++ build tools.

## Choose the build and restore path

Use the repository's validated Visual Studio MSBuild or `devenv` procedure for
mixed solutions. Use `dotnet build/test` where the relevant dependency graph
supports it. Restore the required package formats, including `packages.config`
where used. Preserve solution-to-project configuration and platform mappings.

## Investigate obsolete CLR settings

For a missing `msvcurt.lib`, inspect project settings and build/linker logs for
`/clr:pure` or `CompileAsManaged=Pure` before substituting libraries.
`msvcurt.lib` belongs to the obsolete pure managed CRT; `/clr:pure` has been
unsupported since Visual Studio 2017. This is a diagnostic lead, not proof of
the cause of every missing-library error.

## Scope temporary workarounds

Apply documented or approved overrides only to the intended project and
configuration. C++ `ForceImportBeforeCppProps` and `ForceImportBeforeCppTargets`
imports can support this; check import order and the effective compiler/linker
settings.
Restore previous process environment values in `finally`, including on failure.
Avoid persistent machine settings or production project changes to unblock a
local test build. Changing an executable to a DLL or clearing its entry point
changes the artifact being validated. Restoring environment variables does not
restore build outputs; rebuild normally before producing release artifacts.

## Run the intended tests

Match the test-process architecture to native dependencies. Build the intended
configuration before testing; do not treat an old DLL as current evidence.
Use adapter discovery or a maintained fixture list, not source-code regexes.
When documented process-wide state requires isolation between fixtures, start
a separate runner process for each fixture. `/InIsolation` alone does not
specify a fresh process per fixture.

## Report the scope

Confirm that the intended tests executed; successful exit with zero tests is
not validation. Report commands, configuration, overrides, results, and
intentional exclusions. Distinguish a focused run or agreed subset from the
whole suite and a test-only build from the normal application/release build.

## Sources

- [Discover MSBuild](https://github.com/microsoft/vswhere/wiki/Find-MSBuild)
- [C++/CLI compilation modes](https://learn.microsoft.com/en-us/cpp/dotnet/pure-and-verifiable-code-cpp-cli?view=msvc-170)
- [CRT libraries](https://learn.microsoft.com/en-us/cpp/c-runtime-library/crt-library-features?view=msvc-170)
- [C++ build imports](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-cpp-builds?view=visualstudio)
- [VSTest options](https://learn.microsoft.com/en-us/visualstudio/test/vstest-console-options?view=visualstudio)
