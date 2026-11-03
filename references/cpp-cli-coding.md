# C++/CLI coding guidelines

## Always use braces

**Always use braces for control-flow and scoped statement bodies, even when
they contain one statement. Braceless same-line and next-line forms are both
disallowed.** This includes `if`/`else` and loop bodies. Keep ordinary
`else if` chains, with braces around each branch body.

```cpp
if (isReady)
{
    Start();
}
```

Expand compact function, accessor, type, and try/catch/finally bodies into
blocks with braces on separate lines. Apply the same convention to tests
and stubs.

## Apply the rules to changed code

Apply these rules to new or modified code. Use braces even when nearby legacy
code omits them. Preserve unrelated code. Read the repository's coding
conventions and use features supported by its configured compiler and runtime.
Keep repository-specific naming and architecture rules with that repository.
For build and test commands, follow the [build guide](cpp-cli-builds.md) and
the repository's build instructions.

## Separate native ownership from managed references

Use scoped native owners, such as automatic objects or appropriate smart
pointers, where the containing type permits them. A managed handle (`^`) keeps
a managed object reachable; it does not express ownership of native resources.
Make borrowed pointers and ownership transfers explicit.

Do not embed native class objects, including `std::unique_ptr<T>`, directly
in a `ref class`. Choose a representation compatible with managed types and
give any owned native state a defined cleanup path.

## Release resources deterministically

Use `~Type()` for deterministic disposal of a managed reference type's owned
resources. Add `!Type()` when owned unmanaged resources need fallback cleanup
if disposal is missed. Make repeated disposal safe and prevent double release.
Finalizers must not depend on other managed objects remaining usable.

## Keep pointers and callbacks within their lifetimes

Do not retain a native pointer after the pin or temporary marshaling context
that makes it valid has ended. If a native API retains data, provide storage
whose lifetime covers its use.

Keep a registered callback delegate rooted until native code can no longer
invoke it. A native function pointer alone does not keep the delegate alive.
Coordinate callback unregistration and completion before releasing its state.

## Define interop contracts explicitly

Specify string encoding, buffer lengths, nullability, ownership transfer, and
pointer-sized values at native/managed boundaries. Do not use casts to conceal
incompatible representations or truncate pointers into fixed-width integers.

## Define callback threads and failures

Establish which thread invokes each callback and marshal UI work to the UI's
owning thread. Handle or translate failures according to the boundary's
contract; do not silently lose errors or assume every native caller can
consume a managed exception.

## Sources

- [Native members in managed types (C4368)](https://learn.microsoft.com/en-us/cpp/error-messages/compiler-warnings/compiler-warning-c4368?view=msvc-170)
- [Destructors and finalizers](https://learn.microsoft.com/en-us/cpp/dotnet/how-to-define-and-consume-classes-and-structs-cpp-cli?view=msvc-170#destructors-and-finalizers)
- [Pinning pointer lifetime](https://learn.microsoft.com/en-us/cpp/extensions/pin-ptr-cpp-cli?view=msvc-170)
- [Marshaling context lifetime](https://learn.microsoft.com/en-us/cpp/dotnet/marshal-context-class?view=msvc-170)
- [Callbacks and delegates](https://learn.microsoft.com/en-us/cpp/dotnet/how-to-marshal-callbacks-and-delegates-by-using-cpp-interop?view=msvc-170)
