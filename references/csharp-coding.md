# C# coding guidelines

## Always use braces

**Always use braces for control-flow and scoped statement bodies, even when
they contain one statement. Braceless same-line and next-line forms are both
disallowed.** This includes `if`/`else`, loops, and statements such as
`using (...)`, `lock`, and `fixed`. Keep ordinary `else if` chains, with braces
around each branch body.

```csharp
if (isReady)
{
    Start();
}
```

Expand compact function, accessor, type, and try/catch/finally bodies into
blocks with braces on separate lines. Apply the same convention to tests
and stubs.

Expression-bodied members, expression lambdas, and `using var` declarations
follow repository conventions; this rule does not require converting them.

## Apply the rules to changed code

Apply these rules to new or modified code. Use braces even when nearby legacy
code omits them. Preserve unrelated code. Read the repository's coding
conventions and use features supported by its configured compiler and runtime.
Keep repository-specific naming and architecture rules with that repository.

## Make resource ownership explicit

Dispose resources you own, using `using` or `await using` where supported.
Do not dispose borrowed or container-owned dependencies unless ownership was
explicitly transferred. End subscriptions and timers that can outlive their
owner when that owner's lifetime ends.

## Make asynchronous work observable

Return `Task` or `Task<T>` for asynchronous operations where possible; reserve
`async void` for callbacks whose required signature returns `void`, such as
event handlers. Await work and propagate supported cancellation. Background
work needs an owner, a defined lifetime, and a way to observe failures.
Do not block the UI thread with `.Result`, `.Wait()`, or equivalent synchronous
waits on asynchronous work.

## Preserve useful failures

Catch exceptions when you can recover, translate them for the caller, or add
useful context. Do not hide failures behind empty catch blocks or misleading
success/default results. Use `throw;` to rethrow the current exception while
preserving its original stack trace.

## Make null contracts clear

State when null is legitimate and handle that case explicitly. Express it in
nullable annotations where supported. Use the null-forgiving operator (`!`)
only for an established invariant the compiler cannot prove, not to hide an
unresolved nullability problem.

## Keep types and control flow readable

Use `var` when the type is apparent; use an explicit type when it helps the
reader understand the value or contract. Prefer ordinary loops when mutation,
ordering, or side effects make a LINQ expression harder to follow.

## Optional braces enforcement

A repository can express the braces preference in `.editorconfig`:

```ini
[*.cs]
csharp_prefer_braces = true
dotnet_diagnostic.IDE0011.severity = warning
```

Build enforcement also depends on the project's analyzer configuration.
This example alone does not guarantee that a build reports violations.

## Sources

- [Braces preference (IDE0011)](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/ide0011)
- [Code-style analysis configuration](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview#code-style-analysis)
- [Resource ownership and disposal](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose)
- [Asynchronous programming](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios)
- [Exception handling and rethrowing](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/exception-handling-statements)
