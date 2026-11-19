# Generated `[expected]` wording

Everything in this directory is generated from the `//!` docblocks in
`include/beman/expected/{unexpected,bad_expected_access,expected}.hpp` via
[specgen](https://github.com/steve-downey/specgen). Don't hand-edit it; the
header comments are the source of truth. The exception is `preamble.tex`, the
comment block at the top of `expected.tex`, which is prose about this paper and
is written by hand.

```sh
make wording
```

with `specgen` on `PATH`, or `make SPECGEN=/path/to/specgen wording`. The rule
has real prerequisites, so it does nothing when nothing changed, and `make
papers` regenerates the wording before building the PDF — a paper can no longer
be built from stale clauses.

Those prerequisites are the headers, so a new specgen that renders the same
headers differently leaves make with nothing to do. For that case:

```sh
make clean-wording wording
```

`clean-wording` deletes the fragments, `expected.tex`, and the depfile, and
`wording` writes them all again. It deletes checked-in files, so it refuses to
run when `specgen` is not found, and `make clean` does not reach it.

The run validates the wording and fails on a finding: an error in a docblock,
or a warning, which is something specgen checked and found wrong. The fragments
are written first in either case, so what failed can be read in them. A note
is something specgen cannot check for itself, and does not fail the run.

GNU Make 4.3 or newer. One specgen invocation writes all eight fragments, which
the makefile states as a grouped target (`&:`) — a rule 4.2 parses as something
else entirely, and would then run specgen once per fragment.

specgen writes what it read to `papers/.deps/wording.d`, which the makefile
`-include`s. That is how the dependencies stay honest: it lists every header
each parse touched, including `include/beman/expected/config.hpp`, which none
of the three documented headers names on the command line and which a
hand-maintained prerequisite list would forget.

If embedded Clang cannot locate the C++ standard library, set
`SPECGEN_GCC_TOOLCHAIN` to the GCC installation prefix before regenerating.

## How far it is from the paper and from the draft

```sh
make wording-gap DRAFT_SOURCE=/path/to/draft/source
```

prints two measures and fails on neither. The first is the generated wording
against the paper's hand-written `expected-new.tex`, counted in tokens of code
and of prose, with what a minimal diff leaves on each side. The second is the
change marks specgen makes when it diffs the generated wording against the
working draft, clause by clause, beside the marks the paper makes by hand. A
clause the paper does not change should have none.

`DRAFT_SOURCE` is the `source` directory of a
[cplusplus/draft](https://github.com/cplusplus/draft) checkout; without it the
second measure is skipped. specgen reads whatever revision is there and records
none, so name the revision when quoting the numbers.

## `expected.tex`

All the generated subclauses concatenated in real standard order —
`[expected.general]` and `[expected.syn]`, then `[expected.unexpected]`
(including the new `[expected.un.ref]`) through `[expected.ref.eq]`. The makefile passes `--base-section-depth 2`, so each
`\rSec` marker comes out at the level the draft writes it at:
`[expected.unexpected]` and its siblings are `\rSec2`, their subclauses
`\rSec3`, numbering `22.8.3`, `22.8.3.1`, ... This file is everything that
sits *inside* the existing `\rSec1[expected]{Expected objects}` in
[the draft](https://github.com/cplusplus/draft)'s `source/utilities.tex` — no
wrapper `\rSec1[expected]`, no `\input` directives — so it's the basis for a
patch there: replace the current `[expected.general]` through
`[expected.void]` subclauses with this file's content and the new
`[expected.ref]` subclause lands after them, in place.

`[expected.general]` and `[expected.syn]` come from the top of `expected.hpp`.
The first is a paragraph of section prose. The second is the header synopsis
typed out under `\verbatim-synopsis`, because the draft's header synopsis
forward-declares each class and keeps the class's own synopsis in its
subclause, which is not what gathering the declarations would produce.

The makefile assembles this file from `fragments/` rather than taking
specgen's own joined output, because the clause order is the draft's and not
the headers'. `bad_expected_access<void>` is the base class of
`bad_expected_access<E>`, so the header must define the specialization first,
while the draft states the primary template first. `$(WORDING_CLAUSES)` in the
repository makefile is where that divergence is written down; it is the only
thing about the paper's shape that lives outside the headers.

## `fragments/`

The same content, split one file per top-level clause and named for its stable
name (`expected.general.tex`, `expected.syn.tex`, `expected.unexpected.tex`,
`expected.bad.tex`, `expected.bad.void.tex`, `expected.expected.tex`,
`expected.void.tex`, `expected.ref.tex`) — for
`\input` into a standalone paper's own `\rSec1[expected]{Expected objects}`
(see `papers/expected-new.tex`), which is the level `expected.tex` above
assumes already exists.

specgen also writes a `*.root.tex` per document, holding the declarations that
sit outside every clause: the exposition-only helpers
(*is-unexpected-specialization*, *reinit-expected*,
*converts-from-any-cvref*, and friends). The draft states each of those inline
in the clause that uses it, so they are not part of this paper's wording; the
files are gitignored rather than committed.
