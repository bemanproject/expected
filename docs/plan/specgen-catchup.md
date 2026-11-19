# Plan: specgen-catchup

**Branch:** `specgen-catchup` (from `upstream/main` at `669166b`)
**Read first:** the specgen user guide (`~/src/specgen/main/docs/user-guide.md`,
specgen 0.47.0) and `papers/wording/README.md`.
**Builds on:** [#117](https://github.com/bemanproject/expected/pull/117),
which added `make clean-wording` and regenerated the checked-in wording, with
specgen 0.23.0 and then with 0.41.1 (`b796f6c`). It merged on 2026-11-19 as
`669166b`. This plan's stages start from that wording.
**Measured with:** specgen 0.47.0 (`6c50a01`) on the headers at `396d94d`,
which are the headers on `main`, and the working draft at `65890fab`
(2026-11-17), whose `[expected]` is the same as at `3e3793aa` and `2594eff0`.
**Earlier rounds:** 0.23.0, then 0.41.1 (`9d1689d`) on 2026-11-16, then
0.42.3 and 0.43.0 on 2026-11-17 and 18. Where a number moved, the earlier one
is given beside it.
**Progress:** stages 1 to 6 and 8 are done and are
[#121](https://github.com/bemanproject/expected/pull/121), from the branch
`specgen-catchup`. On the branch `synopsis-shape`, stacked on that one:
[class-prose](#class-prose), [front-matter](#front-matter) and
[api-site](#api-site) are done, and [synopsis-shape](#synopsis-shape) is
done as far as it can go. What is left of it waits on
[reference-error-overloads](#reference-error-overloads) and on specgen, and
[validation-findings](#validation-findings) and
[exposition-helpers](#exposition-helpers) wait with it.
[macro-specifiers](#macro-specifiers) waits on specgen#377.

---

## Goal

Make the generated wording the paper's wording, and make the docblocks say
only what the wording needs said.

Today there are two texts. `papers/expected-new.tex` is what D4280 proposes,
written and change-marked by hand. `papers/wording/` is what specgen renders
from the header docblocks, and it is the declared source of truth, but it is
not what the paper shows and it is not yet draft form. Nothing checks one
against the other.

The end state is:

- the plain render of the headers is the `[expected]` text a working-draft
  pull request would carry, front matter included;
- the paper's marked diff is a specgen render against the working draft, so
  it cannot lag the headers or the draft;
- `generate --validate --warnings-as-errors` passes, and the notes that
  remain have each been read;
- the headers carry no stand-in for something specgen could not do when they
  were annotated, and no second copy of text that is generated;
- the API site built from the same docblocks reads them without warnings
  ([api-site](#api-site)).

A further output is now possible and is the last stage: the draft's own
`utilities.tex` with the paper applied, ready to open as a pull request on
the draft ([draft-edit](#draft-edit)).

## Where this stands with specgen 0.47.0

Three things changed since the plan was last measured, and they reorder it.

**`make wording` fails.** Since 0.44.0 a docblock error fails the run after
the output is written. The seven dead docblocks in `expected<T&, E>` are
docblock errors, so `specgen generate` exits 1 on the headers as they are,
with or without `--validate`. `make wording`, `make wording-check` and
`make papers` all stop there for anyone with a current specgen.
[dead-docblocks](#dead-docblocks) was the third stage and is now the first.

**The eight requests filed on 2026-11-18 are closed.** Each was rerun here.
Seven do what was asked on these headers. The eighth, a macro standing for
`constexpr`, works on a reduced header and not on `bad_expected_access.hpp`,
for a reason found here: the header ends with
`#undef BEMAN_EXPECTED_CONSTEXPR_EXCEPTION`, and specgen reads the macro as
it stands at the end of the translation unit. See
[macro-specifiers](#macro-specifiers).

**The plain render moved, in spelling only.** Against the 0.41.1 wording of
#117 it differs in 42 lines over five fragments, and all 42 are one or two of
three changes: `// exposition only` is written `// \expos`, `\exposidnc{name}` in a
listing is written `\exposid{name}`, and the `&` in the title of
`[expected.un.ref]` is escaped. With those three normalized the two renders
are the same, line for line.

### What specgen gained, and what it does here

| Since | specgen now | Here |
|---|---|---|
| 0.43.1 | two blank `//!` lines before a note, example, code block, list or table give it its own `\pnum` | available to [converge-with-paper](#converge-with-paper), where the draft numbers a note apart from the paragraph before it |
| 0.44.0 | a docblock error exits 1, after the output is written | the build fails until [dead-docblocks](#dead-docblocks); after it, the gate is real ([warning-gate](#warning-gate)) |
| 0.44.1 | the exposition-only comment is the draft's `// \expos` | 14 lines; one artifact gone from the draft diff |
| 0.44.2 | an index entry around a name reads as the name, in the diff | `\libglobal{name}` on a class head is no longer a mark |
| 0.45.0 | an exposition-only name in a listing is `\exposid`, and takes the baseline's form where the two pair | 40 lines |
| 0.45.1 | `&`, `%`, `#` in prose are escaped for LaTeX; `\&`, `\%`, `\#` are read as the characters | the headers have none in prose |
| 0.45.2 | a backticked span in a section title becomes `\tcode{...}`, escaped | the seven titles can be written as prose is ([section-titles](#section-titles)) |
| 0.45.3 | a specifier spelled through a macro is written as its expansion | not here yet, because of the `#undef` ([macro-specifiers](#macro-specifiers)) |
| 0.45.4 | a declaration whose first token is a macro is placed where it is written | with the macro defined, the constructor and `what()` of `[expected.bad]` stay with their class |
| 0.45.5 | `\asdraft` on a namespace-scope exposition-only declaration inherits by declaration | a second way to state a helper ([helper-placement](#helper-placement)) |
| 0.46.0 | `\impldef{...}`, `\ntbs{}`, `\term{...}`, `\defn{...}`, `\Fundescx{...}` are read in docblocks and from the draft | `what()` can be written as the draft has it ([draft-prose-macros](#draft-prose-macros)); importer warnings fall from 11 to 4 |
| 0.46.1 | more of the mathematics inside a `\tcode` is read | no effect on `[expected]` |
| 0.47.0 | `--apply-to-draft` writes the draft's source with the paper applied | fails on these headers, on the two added subclauses ([draft-edit](#draft-edit)) |
| 0.47.1 | under `--warnings-as-errors`, a warning from reading the draft fails the run | not installed here yet; the 4 importer warnings would fail a draft-diff run that passes the flag ([warning-gate](#warning-gate)) |

### Tried on a scratch copy of the headers

Five edits, all markup, none to a declaration:

- the seven in-class docblocks named by the errors deleted;
- `\expos(has_val)` on the three `has_val_` members;
- the seven section titles that name code written with backticks;
- `what()` written `An \impldef{return value of \tcode{...::what}} \ntbs{},`;
- the trailing `#undef` removed, and
  `-D__cpp_lib_constexpr_exceptions=202502L` after the `--`.

With them `generate --validate --warnings-as-errors` exits 0, with no error,
no warning, and the same 124 notes. The seven titles render with `\tcode`.
`\exposid{has_val}` goes from 0 to 27 and nothing else spells the name. The
macro is gone from the wording (9 lines to 0) and `constexpr` stands in its
place. The draft-diff marks for the two clauses the paper does not touch
fall, as the table below shows.

## What exists today

One specgen run over `unexpected.hpp`, `bad_expected_access.hpp` and
`expected.hpp` writes six fragments, and the makefile assembles them into
`papers/wording/expected.tex` in the draft's clause order. `papers/Makefile`
builds `expected-clean.tex` by splicing the hand-written head of
`expected-new.tex` (`[expected.general]`, `[expected.syn]`, markup stripped by
`strip-wording.py`) onto that file. The paper itself `\include`s
`expected-new.tex` and uses no generated text.

The checked-in wording on `main` is specgen 0.41.1's, from #117.

### The gap to the paper, measured

`expected-new.tex` with its markup stripped, against the generated wording,
both from `\rSec2[expected.unexpected]` to the end. The section outline is
identical. Counted by whitespace-separated token, because the paper wraps its
prose by hand and specgen writes a paragraph on one line:

| | paper | generated, 0.23.0 | generated, 0.41.1 |
|---|---|---|---|
| synopses and item declarations | 3290 | 6623 | 4060 |
| of those, only in the paper | | 823 | 845 |
| of those, only in the generated | | 4156 | 1615 |
| prose | 5565 | 7243 | 7243 |
| of that, only in the paper | | 1883 | 1756 |
| of that, only in the generated | | 3561 | 3434 |

No header changed between the two columns. The code that only the generated
wording has fell by three fifths from specgen's changes alone. The prose
barely moved, and is where the work now is.

Not recounted for 0.47.0. The render differs from 0.41.1's only in the three
spellings above, so the prose rows stand and the code rows move by the 14
comment lines.

| | paper | 0.23.0 | 0.41.1 and 0.47.0 |
|---|---|---|---|
| lines in synopses and code blocks | 521 | 1238 | 631 |
| comment lines in them | 22 | 194 | 0 |
| lines with `requires` in them | 4 | 150 | 9 |
| *see below* | 43 | 0 | 0 |
| item declarations | 112 | 165 | 165 |
| numbered paragraphs | 339 | 455 | 455 |
| itemized lists | 34 | 12 | 12 |
| `\exposid{unex}` | 120 | 3 | 131, and 136 in 0.47.0 |
| `\tcode{unex}` | 0 | 79 | 0 |
| `\exposid{has_val}` | 34 | 0 | 0 |
| `BEMAN_EXPECTED_DELETE_MSG` | 0 | 25 | 0 |
| `BEMAN_EXPECTED_CONSTEXPR_EXCEPTION` | 0 | 9 | 9 |

What these say about the render:

- **Comments.** The implementation's comments are gone from the synopses, and
  so are the 22 banner comments, which were never in `// \ref{...}` form. The
  synopses have no group headers at all, until
  [member-routing](#member-routing) writes them.
- **`requires`.** The 9 that remain are on deleted members that have no item
  of their own, where nothing else would state the clause. The paper's 4 are
  different ones: the `operator==` templates, which the draft constrains in
  the declaration. Those want `\constraints-in-decl`.
- **Exposition names.** `unex` and `val` render as exposition-only names from
  the docblocks as they are written. `has_val` does not, because `has_val_`
  derives the name *has-val* and the docblocks and the draft write `has_val`.
  [exposition-names](#exposition-names) names it.
- **Macros.** A deleted tail renders `= delete;`, and the item declaration of
  a deleted member shows it too (16). The macro standing for `constexpr` is
  still printed under its own name, 9 times
  ([macro-specifiers](#macro-specifiers)).
- Still as before: the implementation's overload set where the paper states
  one overload, full `explicit(...)` and `noexcept(...)` conditions where the
  draft writes *see below*, and 53 more item declarations than the paper.

### The gap to the working draft, measured

`--baseline-draft <draft>/source` diffs the generated wording against the
draft's own LaTeX. This is the better yardstick: it compares with the
standard, where the token count above compares with a hand-made copy of it.
Marks in the generated diff, inline added / removed and blocks added /
removed, against the marks the paper makes by hand:

| clause | 0.41.1 | 0.47.0 | 0.47.0, scratch edits | paper: inline, blocks added |
|---|---|---|---|---|
| `[expected.unexpected]` | 17 / 10, 2 / 2 | 15 / 8, 2 / 2 | 15 / 8, 2 / 2 | 1, 1 |
| `[expected.bad]` | 8 / 12, 5 / 2 | 6 / 10, 5 / 2 | 4 / 7, 5 / 2 | 0, 0 |
| `[expected.bad.void]` | 13 / 8, 0 / 1 | 12 / 7, 0 / 1 | 6 / 0, 0 / 1 | 0, 0 |
| `[expected.expected]` | 160 / 111, 46 / 68 | 158 / 109, 46 / 68 | 156 / 107, 46 / 68 | 7, 3 |
| `[expected.void]` | 124 / 84, 33 / 44 | 121 / 81, 33 / 44 | 116 / 76, 33 / 44 | 7, 3 |
| `[expected.ref]` | all new | all new | all new | all new |

specgen's own fixes took two or three marks from each clause. The scratch
edits took more from the two small clauses and little from the large ones,
which is the expected shape: the large clauses differ from the draft in what
they declare and how they group it, and no spelling fix reaches that.

The paper removes nothing, and it does not touch `[expected.bad]` or
`[expected.bad.void]`, so every mark in those two is a difference between the
docblocks and the standard. After the scratch edits, what is left in them is
short enough to list, and each has a stage:

- the six special members of `bad_expected_access<void>` show `= default`
  ([implementation-extras](#implementation-extras));
- the item for `bad_expected_access<void>::what()` lands at the head of
  `[expected.bad]`, ahead of the class synopsis, because its definition
  follows that clause's `\rSec` in the header, and `[expected.bad.void]` has
  no item for it ([member-routing](#member-routing));
- the class's opening prose is a `\remarks` stand-in, where the draft has an
  unlabelled paragraph ([class-prose](#class-prose));
- `(\iref{lex.ccon})` is written with parentheses, where `\iref` prints its
  own ([draft-prose-macros](#draft-prose-macros));
- the constructor's parameter is named in the synopsis (`E e` against `E`);
- the `error()` overloads are declared in another order than the draft's,
  and the draft states two per item ([synopsis-shape](#synopsis-shape)).

Elsewhere, as before: `unexpected`'s constructors show the implementation's
`noexcept(...)`, which the draft does not have, and the deduction guide is
missing from `unexpected`'s synopsis.

One mark is none of these. The draft has `has_error()` on `expected<T, E>`
and `expected<void, E>` (P3798R1, in the draft since 2026-07-15). The library
does not, and the paper's `expected-base.tex` predates it, so the diff shows
it as removed. That is recorded under [diff-baseline](#diff-baseline) and is
not this plan's to fix.

### What validation reports

`generate --validate` prints 132 lines and exits 1:

- **7 errors**, all in `expected<T&, E>`: a docblock on the in-class
  declaration of a member whose definition also carries one. Only the
  definition's is read. The copies have drifted: the copy constructor's
  *Remarks* differ between them. Since 0.44.0 these fail the run.
- **124 notes**: a derived *Constraints* or *Mandates* conjunct with no
  recognized authored counterpart. They fall into three kinds: a conjunct
  that only separates two implementation overloads (`is_reference_v<E>`), an
  opaque predicate the prose states in words
  (`is-expected-specialization<U>::value`), and the class-level
  `static_assert`s against an authored *Mandates* paragraph that states them
  in general terms.
- **0 warnings.**

With `--baseline-draft`, the importer adds 4 warnings of its own (15 in
0.41.1, 11 in 0.42.3): a list item holding a code block in the two
assignment subclauses, and the `floattable` in the two swap subclauses. Both
are [specgen#367](https://github.com/steve-downey/specgen/issues/367), open.

### Whether it compiles

`make papers` builds `D4280R0.pdf`, 39 pages, with no undefined reference
and no overfull box. That is the hand-written `expected-new.tex`.

Nothing compiles the generated wording. Measured with 0.41.1, with
`expected-clean.tex` put in the paper's place on a scratch copy, the build
had one error and 75 overfull boxes, the widest 127pt. The error was the
unescaped `&` in the title of `[expected.un.ref]`, which 0.45.2 escapes. Not
rebuilt with 0.47.0. Of the overfull boxes, 63 were in prose paragraphs,
where a long `\tcode` span does not break, and 12 in item declarations that
wrap later than the paper's. specgen now keeps the draft's line-break hints
(`\brk`, `\-`) where the text is inherited from the draft, and writes none
of its own.

### What the API site makes of the docblocks

`make docs` runs Doxygen over the same headers, and the result is published
to GitHub Pages. Doxygen reads `//!` as its own comment form and knows none
of specgen's markers: `ALIASES` in `docs/Doxyfile` is empty. A run prints 615
warnings, 506 of them for an unknown command:

| Marker | Times |
|---|---|
| `\effects` | 107 |
| `\at` | 79 |
| `\group` | 73 |
| `\also` | 69 |
| `\constraints` | 59 |
| `\mandates` | 41 |
| `\ensures` | 39 |
| `\merge`, `\hardexpects` | 8 each |
| `\item` | 7 |
| `\expos`, `\expects`, `\omit`, `\iref`, `\elsewhere` | 16 together |

Each is dropped from the page with the text after it left as running prose,
so a member's *Effects* reads as an untitled sentence and a routing marker's
argument reads as a stray word. See [api-site](#api-site).

### Stand-ins for what specgen could not do

What the headers write today, and what they can write instead.

| In the headers today | Why, where recorded | Now |
|---|---|---|
| `\remarks` on a class for its opening prose | prose before the first tag was an error | unlabelled leading prose; `\synopsis-here` puts the paragraphs before it ahead of the synopsis |
| `\mandates` on a class for its ill-formed paragraph | only that replaced the derived paragraph | leading prose with `\covers mandates P` replaces it, unlabelled |
| `\at` on every member (79) plus banner comments (22) | not recorded | `// \ref{stable.name}, title` routes the members after it, and is the draft's own synopsis comment |
| `[expected.general]`, `[expected.syn]` written by hand in the paper | no prose without a declaration | section prose; a detached `\verbatim-synopsis` in a `.syn` section is rendered as written |
| rationale for an `\omit`ted member kept after the class | the comment above it leaked into the synopsis | dropped from the synopsis; the rationale can go back above the member |
| `\verbatim-synopsis` for `unexpected<E&>` | not recorded | in-class definitions reduce to declarations; `\merge` removes a twin |
| no `\seebelow` anywhere | not recorded | `\seebelow explicit`, `\seebelow noexcept` |
| exposition names written `unex`, `val` in docblocks, rendered as plain code | not recorded | either spelling renders as the exposition name, anywhere in a code span |
| section titles naming code as plain text | a title was written out as its source | backticks in a title, as in prose |
| "An implementation-defined ntbs" typed as words | the draft's macros were raw text | `\impldef{...} \ntbs{}`, read as the draft's own |
| `(\iref{x})`, and `\iref` after "Subclause" | not recorded | `\iref{x}` prints its parentheses; `\ref{x}` is the bare reference |
| a macro for `constexpr`, printed under its own name | the synopsis took the spelling | the expansion, once the macro is still defined where specgen reads it |
| `/*** ... */` copies of the draft's synopses at the top of the headers (3) | the reference a reader had | the generated synopsis is the reference ([draft-text-copies](#draft-text-copies)) |
| the paper's diff marked by hand | no diff | `--baseline-draft`, and `--baseline-rev`, `--baseline-header`, `--baseline-ir` |
| unchanged wording retyped into docblocks | no other source | `\asdraft` takes an item's description from the draft; `\asdraft-synopsis` a class's synopsis |
| a pull request on the draft made by hand from `expected-clean.tex` | no other way | `--apply-to-draft`, when it can place a new subclause |

### Checked against specgen

The seven scratch headers from the first round of specgen issues, rerun with
0.41.1:

- Plain comments in a class body are dropped from the synopsis, the one above
  an `\omit`ted member included. A `// \ref{x}, title` header and a
  `// \syn ...` comment are kept.
- A `requires`-clause stated as *Constraints* is dropped from the synopsis,
  and kept under `\constraints-in-decl`.
- `= MACRO("...")`, `= delete("...")` and `= delete` all render `= delete;`.
- Leading prose with `\covers mandates` for each asserted predicate replaces
  the derived ill-formed paragraph, and `\synopsis-here` splits the prose
  around the synopsis. Without the claims the derived paragraph still
  renders, before the prose.
- A detached `\verbatim-synopsis` in a `.syn` section is rendered as written,
  with no second namespace, and a declaration after `/// END` is outside the
  section.
- `` `value_ == 0` `` and `` `value == 0` `` both render
  `\tcode{\exposid{value} == 0}`.
- An undescribed member in a synopsis, and a `\ref` header naming a section
  the document does not have, are validation errors that exit 1.

Still true from the first round: `\seebelow noexcept` masks the condition; a
prose-only `//!` block under an `\rSec` renders as that section's paragraphs;
an umbrella header's gathered `.syn` region folds each class's whole synopsis
into the header synopsis.

With 0.47.0, on these headers and on a reduced one:

- A macro whose expansion is `constexpr`, or nothing, is written as its
  expansion in a synopsis and in an item declaration, and a definition that
  begins with one stays with its class. Add `#undef` of the macro at the end
  of the header and it is printed under its own name again.
- A backticked title renders `\tcode{...}`, with `&` escaped inside it.
- `\impldef{...} \ntbs{}` in a docblock renders as the draft's, and the
  diff against the draft pairs the two.
- A docblock error exits 1 with the output written; the last line of
  standard error says how many findings fail the run.

## Stages

Each stage leaves `make wording-check` passing and regenerates the checked-in
wording in the same commit as the header change that caused it. The numbers
are reading order. Stages 1 to 6 are small, are measured above on a scratch
copy, and fit one pull request: after them the run exits 0 under
`--warnings-as-errors`.

### Stage 1 — <a id="dead-docblocks"></a>[dead-docblocks](#dead-docblocks)

Clear the 7 errors, which is what lets anything else be built. For each of
the seven members of `expected<T&, E>` (the in-class declarations at
`expected.hpp` lines 3184, 3205, 3374, 3410, 3450, 3533 and 3547), compare
the in-class docblock with the definition's, settle any difference in the
definition's, and delete the in-class copy. Check: no `error:` line from
`generate`, exit status 0, and the `[expected.ref]` fragment changes only
where a difference was settled.

Done (`1846970`, `0034e47`). Five of the seven pairs said the same thing.
Deleting all seven left the render byte for byte as it was, and the run
exits 0. The other two were the move constructor and the move assignment
operator. Each is the second declaration of a grouped item whose description
is the copy member's, so its exception specification and the condition under
which it is deleted were stated only in the docblock that was never read.
The grouped *Remarks* now state both members' conditions. The paper's
*Remarks* for the constructors says the same in fewer words ("unless that
constructor of `E` is available"), and its assignment item has no *Remarks*
at all; both are [converge-with-paper](#converge-with-paper)'s to settle.

### Stage 2 — <a id="regenerate"></a>[regenerate](#regenerate)

Regenerate the checked-in wording with the current specgen, with no header
change, so that every later diff shows one stage's effect and not specgen's.
Against #117's wording this is the 42 lines of spelling described above.
Then turn on [warning-gate](#warning-gate): there are no warnings to fail
it.

Done once already, for 0.41.1, as the third commit of #117 (`b796f6c`). The
stage recurs whenever specgen changes its render; see
[specgen-pin](#specgen-pin). #117 can merge as it is, with this stage's
commit following it, or take this commit as a fourth. It merged as it was.

Done for 0.47.0 (`3882f08`), with `--warnings-as-errors` in the specgen call
and a paragraph in `papers/wording/README.md` on what fails the run.

### Stage 3 — <a id="gap-yardstick"></a>[gap-yardstick](#gap-yardstick)

Add a goal that prints both measures: the token difference from the stripped
paper wording, and the marks per clause in the diff against the working
draft. It does not fail the build. It needs a draft checkout
([draft-checkout](#draft-checkout)). Every later stage is judged by what it
does to these numbers. The counts in this plan were made by hand each round,
and the scripts were not kept, which is the reason for the goal.

Done (`23188c3`): `make wording-gap DRAFT_SOURCE=<draft>/source`, counted by
`papers/wording-gap.py`. On the 0.41.1 wording it gives the numbers of the
token table above, and for the paper's marks the last column of the draft
table. After stage 6, against the draft at `65890fab`:

| | paper | generated | only in the paper | only in the generated |
|---|---|---|---|---|
| code | 3290 | 4046 | 828 | 1584 |
| prose | 5565 | 7301 | 1711 | 3447 |

| clause | generated: inline added / removed, blocks added / removed |
|---|---|
| `[expected.unexpected]` | 15 / 8, 2 / 2 |
| `[expected.bad]` | 6 / 10, 5 / 2 |
| `[expected.bad.void]` | 12 / 7, 0 / 1 |
| `[expected.expected]` | 155 / 106, 46 / 68 |
| `[expected.void]` | 115 / 75, 33 / 44 |

### Stage 4 — <a id="exposition-names"></a>[exposition-names](#exposition-names)

`\expos(has_val)` on the three `has_val_` members. Check: `\exposid{has_val}`
goes from 0 to 27 and `\tcode{has_val}` to 0. Move the two `\omit` rationales
back above their members.

Done (`cf465bd`). 27, and 0. The note on the deleted copy assignment is
above the primary template's `\omit`ted overload, and the note on `void_` is
above that member in the union. Neither changed the wording.

### Stage 5 — <a id="section-titles"></a>[section-titles](#section-titles)

Write the 7 titles that name code with backticks, as prose does:
``{Partial specialization `unexpected<E&>`}``. Check: each renders with
`\tcode{...}` and matches the paper's title.

Done (`54989d4`). Every heading of the generated wording, title and stable
name, is now the same as the paper's.

### Stage 6 — <a id="draft-prose-macros"></a>[draft-prose-macros](#draft-prose-macros)

Write the draft's own macros where the docblocks now spell their meaning in
words or get them slightly wrong:

- `what()`, twice: `An \impldef{return value of
  \tcode{bad_expected_access<void>::what}} \ntbs{},`, with the index text the
  draft has for each;
- `\iref{lex.ccon}` without the parentheses around it, twice, and
  `Subclause \ref{expected.unexpected}` for the one `\iref` that follows the
  word "Subclause";
- any `\term`, `\defn` or named requirement the draft uses in text the
  docblocks retype, found by reading the draft diff for the marks they leave.

Check: the sentences changed read as the draft's do, and no other paragraph
of the plain render changes.

Done (`f22e465`). `what()` twice; `\iref{lex.ccon}` twice, written
`encoding\iref{lex.ccon}` with no space before it, as the draft does, since
the macro prints its own; `\ref` after "Subclause"; and three sentences the
docblocks share with the draft: `\cv{}` before `bool` in two *Constraints*,
`\Fundescx{Effects}` in two *Throws*, `\iref{intro.object}` after "nested
within" in two class descriptions. The draft's `\term{valid value type for
\tcode{expected}}` and its `\oldconcept{Destructible}` requirements are in
paragraphs the docblocks do not have in that form, and go with
[class-prose](#class-prose).

The check first written here was wrong. It expected the marks in
`[expected.bad]` and `[expected.bad.void]` to fall as in the scratch column,
but that fall came from the macro define, which is
[macro-specifiers](#macro-specifiers). The two `what()` items still show as
one block removed and one added, because the item does not pair with the
draft's while it lacks `constexpr` and sits in another place. Their text is
now the draft's, so they will pair clean when those two are settled.

### Stage 7 — <a id="macro-specifiers"></a>[macro-specifiers](#macro-specifiers)

Have the wording show `constexpr` where the header writes
`BEMAN_EXPECTED_CONSTEXPR_EXCEPTION`. Two parts. The run names the expansion
the wording wants ([macro-expansion-args](#macro-expansion-args)). And the
macro has to be defined where specgen reads it, which the trailing `#undef`
prevents: that is
[specgen#377](https://github.com/steve-downey/specgen/issues/377), and the
stage waits for it. Check: the macro appears 0 times in the wording, and
`[expected.bad.void]` is left with the `= default` marks alone.

### Stage 8 — <a id="member-routing"></a>[member-routing](#member-routing)

Replace the banner comments with `// \ref{stable.name}, title` group
comments, in the paper's spelling, and drop each `\at` that the group now
implies. `\at` stays where a member sits outside its group, and one is
added: `bad_expected_access<void>::what()` is routed to
`[expected.bad.void]`. Check: item placement is unchanged but for that one,
and the synopses gain the paper's 22 group headers.

Done (`081b893`). 21 banners in the three `expected` classes became group
comments and `unexpected` gained its one, 22 in all; 56 `\at` markers went,
and 16 remain: 14 in `unexpected.hpp`, whose members after the constructors
sit outside any group in the draft's synopsis, and the two that place a
class's own wording in its `.general` subclause. The wording gained the 22
comment lines and lost nothing. `\at` does not route an out-of-line
definition, so `bad_expected_access<void>::what()` was moved instead: its
definition now follows its class, ahead of the section comment for the
primary template. `[expected.bad]` opens with its synopsis and
`[expected.bad.void]` has its item, and the removed block in that clause's
draft diff is gone. Code only in the generated wording is 1576 tokens, and
only in the paper 748.

### Stage 9 — <a id="synopsis-shape"></a>[synopsis-shape](#synopsis-shape)

Bring the class synopses to the draft's shape. What is left of it:

- `\seebelow explicit` and `\seebelow noexcept` where the paper writes
  *see below* (43 occurrences);
- one overload where the implementation has several
  ([overload-partitions](#overload-partitions));
- `\constraints-in-decl` on the `operator==` templates;
- declaration order and grouping where the draft's differs, the `error()`
  overloads first;
- `unexpected<E&>` tried without its `\verbatim-synopsis`, and the deduction
  guide in `unexpected`'s synopsis;
- what the implementation declares beyond the draft
  ([implementation-extras](#implementation-extras)).

Then [draft-text-copies](#draft-text-copies).

Under way, on the branch `synopsis-shape`. Done so far:

- *see below* on the sixteen members whose item declaration has it in the
  paper (`05f014c`). Where the draft's synopsis says *see below* and its item
  declaration spells the condition out, as for `expected(U&& v)`, the
  condition stays: one marker masks both places.
- The trivial twins of the special members, in the primary template and in
  `expected<T&, E>`, are `\merge` (`ab56679`), as they were in
  `expected<void, E>`. The survivors' *Constraints* are the paper's in all
  three classes: an authored list for the move members, and an empty
  `\constraints` for the copy members and the destructors, which the paper
  states in *Remarks*. Item declarations fall from 165 to 153.
- `\constraints-in-decl` on the first `operator==` of each class, and
  `\freestanding-deleted` on `value()` (`cae7873`).
- `bad_expected_access<E>::error()` is two items of two overloads. Its draft
  marks are 3 / 3, 2 / 2, from 6 / 10, 4 / 2.
- `unexpected<E&>` has its synopsis extracted (`994273f`), and it declares
  what the typed one did.

Against the draft at `65890fab` after these: `[expected.expected]` 124 / 71,
43 / 69 and `[expected.void]` 99 / 57, 34 / 46. Code only in the generated
wording is 1303 tokens, from 1576, and prose 2870, from 3428.

Not done, and why:

- The reference-`E` twins and the deleted overloads are not merged. The
  paper says nothing about them, so there is no survivor wording to carry
  what they say: [reference-error-overloads](#reference-error-overloads).
- What the implementation declares beyond the draft, a strengthened
  `noexcept`, `= default`, a parameter name in the synopsis, has no markup:
  specgen#385.
- The deduction guide is not in `unexpected`'s synopsis: specgen#384.
- The item for `bad_expected_access<E>::what()` follows the order of the
  class's declarations and is second, where the draft has it last.
- "Assignment rebinds", the paragraph that opens `[expected.ref.assign]`, is
  section prose now and renders after the subclause's items: specgen#383.
- [draft-text-copies](#draft-text-copies), until the synopses of
  `bad_expected_access` match the draft's, which waits on specgen#377 and
  specgen#385.

### Stage 10 — <a id="class-prose"></a>[class-prose](#class-prose)

Rewrite the general subclauses as the draft has them: unlabelled paragraphs
in the draft's order, split around the synopsis with `\synopsis-here`, in
place of the `\remarks` and `\mandates` stand-ins. See
[class-ill-formed-paragraph](#class-ill-formed-paragraph).

Done (`a27005c`). The six class docblocks are the paper's paragraphs in the
paper's order. `unexpected` opens its subclause ahead of the synopsis; the
others have all their prose after it, as the paper does. Each ill-formed
sentence has a `\covers mandates` claim for every `static_assert` of its
class, 30 in all, and the notes fell from 138 to 108. Three paragraphs came
in from the paper that the docblocks lacked: the definition of a valid value
type for `expected`, and the *Cpp17Destructible* requirements in the three
`expected` classes. Two sentences keep what the assertions enforce where the
paper says less, and are [converge-with-paper](#converge-with-paper)'s:
`unexpected<E&>` names a non-object referenced type, and `expected<T&, E>`
lists `in_place_t`, `unexpect_t` and specializations of `unexpected` for
`T`. Prose only in the paper fell from 1690 tokens to 1369.

### Stage 11 — <a id="validation-findings"></a>[validation-findings](#validation-findings)

Read the 124 notes and answer each. The three kinds have different answers:

- an opaque predicate stated in prose gets `\covers`;
- an overload-partition conjunct goes away with
  [overload-partitions](#overload-partitions), so this stage follows
  [synopsis-shape](#synopsis-shape);
- the class-level ones go away with [class-prose](#class-prose);
- anything left is a real difference between the code and the authored
  wording, and is fixed in whichever is wrong.

Not started. 108 notes after [class-prose](#class-prose). By kind: 18 are
`is_reference_v<E>`, the conjunct that separates a reference-`E` twin, and go
with [reference-error-overloads](#reference-error-overloads); about ten are
the trivial traits of a merged special member, or a condition its *Remarks*
state, which need specgen#386; the rest are opaque predicates and the
monadic operations' requirements, each of which wants its item read. The
stage keeps its place after [synopsis-shape](#synopsis-shape).

### Stage 12 — <a id="front-matter"></a>[front-matter](#front-matter)

Generate `[expected.general]` and `[expected.syn]`, add them to
`$(WORDING_CLAUSES)`, and retire the head splice in `papers/Makefile` and
`strip-wording.py`'s part in it. See
[header-synopsis-form](#header-synopsis-form).

Done (`2c1c551`). `expected.hpp` opens with the general paragraph as section
prose and the header synopsis under `\verbatim-synopsis`, in place of the
block comment that held a copy of the draft's text. The two fragments are in
`$(WORDING_CLAUSES)`, and the generated text is the paper's token for token,
less the three `\index...` lines the paper has ahead of the synopsis.
`expected-clean.tex` is the clause heading and the generated wording.
`strip-wording.py` stays for `wording-gap`, which strips the paper's markup
to compare with, until [generated-diff](#generated-diff) retires both.

### Stage 13 — <a id="exposition-helpers"></a>[exposition-helpers](#exposition-helpers)

Today the `*.root.tex` fragments hold the exposition-only helpers and are
thrown away, so the generated wording uses `unexpect-dangles-v` and defines
it nowhere. Decide per helper, under [helper-placement](#helper-placement),
whether the wording defines it in the clause that uses it or stops naming it.
`--apply-to-draft` counts these too: it leaves out eight declarations that
are in no subclause, with a warning each.

Not started. Two of the helpers cannot be settled yet.
*unexpect-dangles-v* is named only by the overloads that
[reference-error-overloads](#reference-error-overloads) asks about. And
*reinit-expected* has to be defined in a paragraph that opens
`[expected.object.assign]`, which is where specgen#383 puts section prose
last. Moving its definition under that subclause's section comment is also a
change to where code is, the first in this plan that is more than one inline
function.

### Stage 14 — <a id="api-site"></a>[api-site](#api-site)

Make the Doxygen build read the docblocks. Independent of the other stages,
and can go any time after stage 2. See
[api-site-markup](#api-site-markup). Check: no "unknown command" warning
from `make docs`, and an *Effects* paragraph on the page carries its title.

Done (`35a6724`). Warnings from the headers went from 592 to 93, all of
them members with no documentation, and none is an unknown command. A
member's page shows *Constraints*, *Effects* and the rest as titled
paragraphs, a `\item` list as a list, and an overload joined with `\also` as
an overload of the one before it. Tried with Doxygen 1.15.0 writing to a
scratch directory. The workflow that publishes the site runs on merge and
has not run with it.

### Stage 15 — <a id="converge-with-paper"></a>[converge-with-paper](#converge-with-paper)

Work both [gap-yardstick](#gap-yardstick) measures down. The target for the
draft diff is the paper's own marks: nothing in `[expected.bad]` and
`[expected.bad.void]`, and in the other clauses the additions the paper makes
and no removals. Each remaining difference is settled in the header or in the
paper, whichever is wrong, or written down as intended. The generated wording
also has to compile in the paper's place without overfull boxes; it had 75.
The paper's itemized lists (34 against 12) are the systematic difference
already known to belong here. This is the gate for the next stage: until the
generated diff says what the paper's hand-marked diff says, including it
would change what the paper proposes.

### Stage 16 — <a id="generated-diff"></a>[generated-diff](#generated-diff)

Render the paper's marked wording with specgen and have `D4280R0.tex`
include that. `expected-new.tex`, `expected-base.tex` and
`strip-wording.py` are retired, and `expected-clean.tex` becomes the plain
render. `--section-number` gives the fragments' headings their draft numbers.
See [diff-baseline](#diff-baseline).

### Stage 17 — <a id="draft-edit"></a>[draft-edit](#draft-edit)

Produce the draft's `utilities.tex` with the paper applied, with
`--apply-to-draft`, as a goal beside the paper's. See
[draft-pull-request](#draft-pull-request). It waits on specgen and on
[converge-with-paper](#converge-with-paper): an edit of the draft is only as
small as the diff against it.

## Decisions

Entry shape: Question / Status / Recommendation or Decision / Why / Log.

### synopsis-source

**Question.** Are the class synopses extracted from the class bodies, or
authored with `\verbatim-synopsis`?
**Status.** OPEN
**Recommendation.** Extracted. Nothing in specgen stands in the way now.
**Why.** Extraction is the point of the tool: an authored synopsis is a
second copy of every declaration. specgen now drops from the synopsis the
`requires`-clause it states as *Constraints*, which was the one thing
extraction could not reach, and checks a `\verbatim-synopsis` against its
class under `--validate`, which lowers the cost of the alternative.
`\asdraft-synopsis` is a third form: the draft's synopsis text, with the
specifiers taken from the declarations. It suits a class the paper barely
changes, and none of the three large classes is one.
**Log.**
- 2026-11-16: opened. `requires` in synopses: 150 lines against the paper's 4.
- 2026-11-16: specgen 0.41.1 drops the clause (specgen#281). 9 lines remain,
  all on deleted members with no item.
- 2026-11-19: 0.47.0. `bad_expected_access<void>` is a class the paper does
  not change, and after the scratch edits its extracted synopsis differs from
  the draft's by six `= default` alone. It is the one candidate for
  `\asdraft-synopsis`, if [implementation-extras](#implementation-extras)
  finds no other way to drop them.

### overload-partitions

**Question.** Where the implementation splits one specified overload into
several (trivial and non-trivial, value-`E` and reference-`E`), what does the
wording show?
**Status.** DECIDED
**Decision.** One overload, as the paper has it: the survivor carries
the wording and each twin is `\merge`d.
**Decided by.** Steve Downey, 2026-11-19: take the recommendation for
[synopsis-shape](#synopsis-shape).
**Why.** The paper's synopsis is the specification, and the split is how this
library implements it. specgen's `\merge` drops the conjunct that only
separates a survivor from its twin, but only when the twin states the
other half. The defaulted copy and move constructors here are unconstrained
on purpose, so the survivor's `!(A && B)` has nothing to pair with and its
*Constraints* are authored.
**Log.**
- 2026-11-16: opened.
- 2026-11-19: `--apply-to-draft` names where the split shows against the
  draft: one declaration removed from an item and three added in
  `[expected.object.cons]`, one removed in `[expected.object.assign]`, two
  removed in `[expected.bad]`, and fourteen items added in
  `[expected.void.cons]` and `[expected.void.dtor]`, where the draft groups
  what the docblocks state one by one.
- 2026-11-19: decided. Applied to the trivial twins of the primary template
  and `expected<T&, E>` (`ab56679`). The survivor's `requires`-clause still
  names the split, so its *Constraints* are authored; where the paper has no
  *Constraints* element the docblock has an empty `\constraints`, which
  removes the derived one (specgen#386 asks that this be documented, and
  that *Remarks* be able to cover a derived conjunct: the notes went from
  124 to 138). Not applied to the reference-`E` twins:
  [reference-error-overloads](#reference-error-overloads).

### implementation-comments

**Question.** Where do the implementation's comments in a class body go?
**Status.** DECIDED
**Decision.** They stay where they are, as plain `//`. The synopsis keeps a
`// \ref{...}` group header and a comment marked `// \syn`, and drops the
rest.
**Why.** Not being able to comment inside a class is a burden on the code,
so the fix belonged in the tool. The draft's synopses do carry comments: of
about 4058 comment lines in the library clauses, about five in six are group
headers, `exposition only`, freestanding marks and *see below*, which specgen
reads or writes itself, and about one in six is free text, which is what the
marker is for.
**Decided by.** Steve Downey, 2026-11-16, as the direction for specgen#280.
**Log.**
- 2026-11-16: opened, with 194 comment lines in the synopses against 22.
- 2026-11-16: Steve Downey: filter comments out of the synopsis, perhaps
  with markup for any that should be reproduced; not being able to comment
  in a class in real code is a real burden. Filed as specgen#280.
- 2026-11-16: specgen 0.41.1 does this. 0 comment lines in the synopses,
  with no header change. No comment here needs `\syn` that is known yet.

### deleted-message-spelling

**Question.** How does a member deleted through
`BEMAN_EXPECTED_DELETE_MSG("...")` appear in the wording?
**Status.** OPEN
**Recommendation.** Not at all where the paper states the deletion in a
*Remarks* on the enabled overload (`\merge`), and as `= delete;` where the
paper declares the deleted member.
**Why.** The spelling half is settled by specgen: the tail renders
`= delete;` whatever the header writes. What is left is which deleted members
the wording declares at all, and that follows the paper.
**Log.**
- 2026-11-16: opened. The macro appeared 25 times.
- 2026-11-16: specgen 0.41.1 renders `= delete;` (specgen#282). 0 times.
- 2026-11-19: not applied yet. The paper neither declares these members
  nor states their deletion in a *Remarks* on the enabled overload, so
  neither half of the recommendation has anything to follow:
  [reference-error-overloads](#reference-error-overloads).
- 2026-11-19: three of the fourteen items `--apply-to-draft` reports as added
  in `[expected.void.cons]` are deleted overloads, which the draft does not
  declare.

### class-ill-formed-paragraph

**Question.** How is a class's "a program that instantiates ... is
ill-formed" paragraph stated?
**Status.** OPEN
**Recommendation.** As the draft's own sentence, in unlabelled leading prose,
with `\covers mandates P` for each `static_assert` it speaks for.
**Why.** The draft writes it as an unlabelled paragraph. The claims keep the
assertions as the evidence the sentence is checked against, and a predicate
the sentence does not cover stays a note.
**Log.**
- 2026-11-16: opened. Only an authored `\mandates` replaced the derived
  paragraph, with a label.
- 2026-11-16: specgen 0.41.1 has `\covers mandates` on a class (specgen#283)
  and `\synopsis-here`. Recommendation changed from keeping `\mandates`.
- 2026-11-19: applied as recommended in [class-prose](#class-prose)
  (`a27005c`), to all six classes. Not ruled on.

### warning-gate

**Question.** Does a validation warning fail `make wording` and
`make wording-check`?
**Status.** OPEN
**Recommendation.** Yes: add `--warnings-as-errors` to the specgen call in
the makefile, in [regenerate](#regenerate). Leave it off the goals that read
the draft until specgen#367 is closed.
**Why.** A warning is something specgen verified, and there are none, so the
gate costs nothing and catches the first one. The 124 notes do not fail it
and are worked through in [validation-findings](#validation-findings).
Docblock errors now fail the run by themselves, so the gate no longer has to
look for `error:` on standard error. From 0.47.1 the flag also covers
warnings from reading the draft, and there are 4 of those here that no
header change can clear.
**Log.**
- 2026-11-16: opened. 124 warnings, and specgen exited 0 on warnings.
- 2026-11-16: Steve Downey: warnings and notes need to be distinguished
  better; a note is something that has to be checked externally, and some
  messages are for things the tool cannot verify. Filed as specgen#285.
- 2026-11-16: specgen 0.41.1: the 124 are notes, and `--warnings-as-errors`
  exists and passes.
- 2026-11-19: specgen 0.44.0 exits 1 on a docblock error (specgen#350), so
  the run fails today, flag or no flag. On the scratch headers
  `--validate --warnings-as-errors` exits 0.
- 2026-11-19: the flag is in the makefile's specgen call (`3882f08`), as
  recommended, and off the draft diff in `wording-gap`. Applied in carrying
  out [regenerate](#regenerate); not ruled on.

### header-synopsis-form

**Question.** How is `[expected.syn]` generated?
**Status.** OPEN
**Recommendation.** A detached `\verbatim-synopsis` in an
`\rSec2[expected.syn]` section of `expected.hpp`, replacing the `/*** */`
copy of the draft text that is there now.
**Why.** The gathered `.syn` region folds each class's full synopsis into the
header synopsis, where the draft has a forward declaration and keeps the
synopsis in the class's own clause. The verbatim form gives the draft's
text, and specgen's guide now names it as the form for a header whose
content is classes.
**Log.**
- 2026-11-16: opened, with two defects in the way.
- 2026-11-16: both fixed in specgen 0.41.1 (specgen#284).
- 2026-11-19: applied as recommended in [front-matter](#front-matter)
  (`2c1c551`). Not ruled on. A `// \ref{...}` comment and a `\tcode{...}` in
  the typed synopsis are written out as they stand, which is what the
  draft's source has.

### draft-text-copies

**Question.** Do the headers keep the `/*** ... */` copies of the draft's
synopses at the top of the file?
**Status.** OPEN
**Recommendation.** No. Each goes when the generated synopsis of its class
matches the draft's: the two in `bad_expected_access.hpp` after
[synopsis-shape](#synopsis-shape), and the one in `expected.hpp` with
[front-matter](#front-matter), where
[header-synopsis-form](#header-synopsis-form) turns it into the source of
`[expected.syn]`.
**Why.** They were the reference a reader of the header had before there was
generated wording. Now they are a third copy of each synopsis, after the
class body and the generated text, and the only one nothing checks. The
draft diff is the check that the class agrees with the standard.
**Log.**
- 2026-11-19: opened. Three blocks: `bad_expected_access.hpp` lines 18 and
  38, `expected.hpp` line 26.
- 2026-11-19: the one in `expected.hpp` is gone, replaced by the source of
  `[expected.syn]` (`2c1c551`). The two in `bad_expected_access.hpp` stay
  until the generated synopses there match the draft's.

### clause-order

**Question.** Does the makefile keep assembling `expected.tex` in
`$(WORDING_CLAUSES)` order?
**Status.** OPEN
**Recommendation.** Yes.
**Why.** The one divergence it records, `[expected.bad]` before
`[expected.bad.void]`, could be had from an umbrella header's `\rSec`
outline instead, but only together with the gathered synopsis that
[header-synopsis-form](#header-synopsis-form) recommends against.
**Log.**
- 2026-11-16: opened, after the scratch-header check.

### helper-placement

**Question.** Where does the wording define an exposition-only helper?
**Status.** OPEN
**Recommendation.** In the clause that first uses it, by opening that
clause's `\rSec` before the helper's declaration, for the helpers the paper
keeps. A helper the paper does not name is restated in the authored wording
instead.
**Why.** A declaration before the first `\rSec` goes to the root fragment,
and the makefile does not assemble those. `reinit_expected` renders there
under its C++ name, as an indexed library function, while the draft shows
*reinit-expected* as code inside `[expected.object.assign]`.
**Log.**
- 2026-11-16: opened. Unchanged in 0.41.1.
- 2026-11-19: 0.45.5 lets `\asdraft` on a namespace-scope exposition-only
  declaration inherit the draft's text by its declaration, which would suit
  *reinit-expected*, at the price of a draft checkout for the plain render
  ([unchanged-wording-source](#unchanged-wording-source)). And
  `--apply-to-draft` has no place for a declaration outside every subclause:
  it leaves out eight here. Both point the same way as the recommendation.

### implementation-extras

**Question.** Where the implementation declares more than the draft
specifies, what does the wording show?
**Status.** DECIDED
**Decision.** The draft's declaration. How, case by case:
`\seebelow` cannot do it, since the draft has no *see below* there, so it is
`\verbatim-itemdecl` and the synopsis's counterpart, or a request to specgen.
**Why.** The diff against the draft shows three cases in clauses the paper
does not change: a conditional `noexcept` on `unexpected`'s constructors,
`= default` on the special members of `bad_expected_access<void>`, and
`BEMAN_EXPECTED_CONSTEXPR_EXCEPTION` where the draft has `constexpr`. The
first two are permitted strengthenings that are not wording. The third is a
spelling, of the kind specgen#282 settled for `= delete`.
**Decided by.** Steve Downey, 2026-11-19: take the recommendation for
[synopsis-shape](#synopsis-shape).
**Log.**
- 2026-11-16: opened, from the first `--baseline-draft` run.
- 2026-11-19: the third case has its own stage,
  [macro-specifiers](#macro-specifiers): specgen#349 writes the expansion,
  but not for a macro the header `#undef`s. Two cases remain here. A fourth
  is small enough to settle with them: the constructor of
  `bad_expected_access<E>` names its parameter in the synopsis, and the
  draft does not.
- 2026-11-19: decided, and it is a request to specgen in all three cases
  (specgen#385). `\verbatim-itemdecl` would fix an item declaration and leave
  the synopsis as it is, and `\verbatim-synopsis` for a whole class to drop
  one `noexcept` gives up more than it gains. The same holds for the copy
  constructors and copy assignment operators of the three `expected`
  classes, which the library declares `noexcept(...)` and the draft does
  not. Nothing is changed in the headers until specgen has a marker.

### macro-expansion-args

**Question.** Which expansion of a configuration macro does the wording
show, and where does the build say so?
**Status.** OPEN
**Recommendation.** The expansion the standard has: `constexpr`, by adding
`-D__cpp_lib_constexpr_exceptions=202502L` to `SPECGEN_CLANG_ARGS`.
**Why.** specgen writes what the macro expands to in the translation unit it
parses, so the wording follows whichever standard library and compiler
specgen's Clang happens to find. Today that is the empty expansion, and the
wording would lose `constexpr` from nine declarations the draft marks with
it. Stating the macro on the command line makes the render the same on every
machine, and the value is the one libstdc++ 16 defines. The cost is that the
wording run and a real build may then parse the header differently, which is
what the option is for.
**Log.**
- 2026-11-19: opened. With the define and the `#undef` removed, on scratch,
  the macro appears 0 times and `constexpr` stands in its place.

### unchanged-wording-source

**Question.** Is wording the paper does not change authored in the
docblocks, or inherited from the draft with `\asdraft`?
**Status.** OPEN
**Recommendation.** Authored, with the diff against the draft as the check
that it has not drifted. `\asdraft` for an item whose draft text the docblock
cannot state.
**Why.** The docblock is where a reader of the header finds what a member is
specified to do, and an `\asdraft` item says only that the draft has it.
Inheriting also makes the plain render need a draft checkout
(`--inherit-draft`), where today it needs only the headers. Against that,
inheriting is the only way unchanged text cannot drift, and the draft diff
makes drift visible without it.
**Log.**
- 2026-11-16: opened. Not tried on these headers yet. The items the importer
  kept as raw LaTeX were the candidates for `\asdraft`: `what()` with
  `\impldef` and `\ntbs`, the swap tables, a nested list in the assignment
  subclauses.
- 2026-11-19: 0.46.0 reads `\impldef`, `\ntbs` and `\term`, in the draft and
  in a docblock, so `what()` is authored
  ([draft-prose-macros](#draft-prose-macros)) and is no longer a candidate.
  The swap tables and the list holding a code block still are
  (specgen#367).

### draft-checkout

**Question.** Where does the build find the working draft, and at which
revision?
**Status.** OPEN
**Recommendation.** A make variable naming a draft checkout's `source`
directory, used only by the goals that diff against the draft. The revision
is named in the paper and recorded next to the variable. `make wording`
stays independent of it unless
[unchanged-wording-source](#unchanged-wording-source) goes the other way.
**Why.** specgen records no draft revision; it reads whatever the directory
holds, and lists the files in the depfile.
**Log.**
- 2026-11-16: opened. Numbers against `2594eff0`.
- 2026-11-19: numbers against `65890fab` (2026-11-17), from a
  `git archive` of that revision into a scratch directory, since the local
  checkout sits at N5054. `utilities.tex` does not differ between
  `3e3793aa` and `65890fab`.
- 2026-11-19: `DRAFT_SOURCE` is the variable (`23188c3`), read only by
  `wording-gap`, which skips the draft measure when it is unset. Where the
  revision is recorded is still open.

### diff-baseline

**Question.** What is the baseline for the paper's generated diff?
**Status.** OPEN
**Recommendation.** The working draft, with `--baseline-draft`, at the
revision [draft-checkout](#draft-checkout) names.
**Why.** It is the thing the paper proposes to change, and it needs no
baseline header set and no committed IR, which is what the first
recommendation here had to build. A section the draft lacks, `[expected.ref]`
and `[expected.un.ref]`, renders as all added. The cost is that the diff is
only as clean as the plain render is close to the draft, which is what
[converge-with-paper](#converge-with-paper) is for.
The draft has moved since the paper's base was taken: `has_error()` is in
`[expected.object.obs]` and `[expected.void.obs]`, and the `expected<void>`
synopsis is wrapped in `namespace std`. A diff against today's draft
therefore shows `has_error()` removed until the library and the paper catch
up with P3798R1, or the baseline is pinned to a draft before it.
**Log.**
- 2026-11-16: opened, recommending a baseline header set read through
  `--baseline-ir` for R0, since no revision of the annotated headers renders
  the working draft (docblocks `85e6712`, 2026-09-08; reference support
  `db1c54b`, 2026-07-04).
- 2026-11-16: specgen 0.41.1 has `--baseline-draft`; it runs on these
  headers. Recommendation changed. `expected-base.tex` differs from the draft
  at `2594eff0` by `has_error()` and the reindented `expected<void>`
  synopsis.
- 2026-11-19: 0.47.0. Two artifacts of the comparison are gone
  (specgen#353, specgen#354), and the marks per clause are in the table
  above.

### draft-pull-request

**Question.** Is the paper's change also produced as an edit of the draft's
source?
**Status.** OPEN
**Recommendation.** Yes, as the last stage, once specgen can place an added
subclause. Nothing is built for it before then.
**Why.** It is what the editors apply, and specgen makes it from the same
headers, changing only the bytes that change, so the paper, the clean text
and the pull request cannot disagree. This paper's main content is two new
subclauses, `[expected.ref]` and `[expected.un.ref]`, and placing an added
subclause is the part of specgen#346 not yet done. The run also stops on an
internal error after listing what it cannot place, so nothing is written.
**Log.**
- 2026-11-19: opened. `--apply-to-draft` on the headers as they are: 23
  changes it cannot place (2 added subclauses, 14 added items, 3 added and 4
  removed declarations inside an item), 8 declarations outside every
  subclause left out, then
  `an edit of bytes 244560 to 244560 overlaps another or runs past the end`
  and no file. Most of the 23 are
  [overload-partitions](#overload-partitions) and
  [synopsis-shape](#synopsis-shape) seen from the draft's side.
- 2026-11-19: filed as specgen#378. The offset is directly before `public:`
  in the synopsis of `expected<T, E>`, where the header adds a private
  exposition-only alias. A small case of the same shape does not abort, but
  writes the added tokens on the draft's line, so that `public:` ends up
  inside the `// \expos` comment.

### api-site-markup

**Question.** How does the API site read docblocks written for specgen?
**Status.** OPEN
**Recommendation.** `ALIASES` in `docs/Doxyfile`: each element tag
(`\effects`, `\constraints`, `\mandates`, `\ensures`, `\expects`,
`\hardexpects`) becomes a titled paragraph, and each marker (`\at`,
`\group`, `\also`, `\merge`, `\omit`, `\expos`, `\elsewhere`) becomes
nothing. Try it first: a Doxygen alias takes its arguments in braces, and
`\at stable.name` passes its argument as the next word, so the markers that
take one may need a filter in place of an alias.
**Why.** The published pages are built from the headers by Doxygen, and
that is not changing in this plan. The docblocks cannot be written for both
readers by hand, so the mapping belongs in configuration. The alternatives
are an `INPUT_FILTER` that rewrites the markers, which handles the
arguments but is a second parser of the markup, and building the reference
pages from specgen's own `mpark` or `org` output, which is a different site.
A set of aliases that specgen shipped would serve every project that uses
it, and is worth asking for once it is known to work here.
**Log.**
- 2026-11-19: opened. 506 unknown-command warnings from `make docs`, by
  marker in the table above.
- 2026-11-19: both, each for what it can do (`35a6724`). `ALIASES` for the
  six element tags and `\item`. An input filter for the headers,
  `docs/specgen-doxygen-filter.py`, for the markers that take the rest of
  the line, for `\verbatim-synopsis`, and for the draft's braced macros,
  whose arguments nest and hold commas. Aliases alone were not tried
  further once the markers had to be filtered anyway. Not ruled on.
  Separately, Doxygen's input includes `docs/`, so it reads this plan too
  and warns 54 times about its slug links; `docs/plan/extract-xfail-compile.md`
  draws ten of the same. Whether plans belong on the site is not this
  stage's question.

### reference-error-overloads

**Question.** The headers specify overloads for a reference `E` that the
paper's wording for `expected<T, E>` and `expected<void, E>` does not
mention. Which is wrong?
**Status.** OPEN
**Recommendation.** The paper. It should state them, in the item of the
overload each one qualifies, and then the twins merge into that item as
[overload-partitions](#overload-partitions) decides.
**Why.** These are what keeps an `expected<T, E&>` from holding a dangling
reference, which is the paper's own design, and the library implements and
tests them. The paper changes `[expected.object.cons]` and
`[expected.object.assign]` only to add "or `is_reference_v<E>` is `true`" to
the conditions of the copy and move members and a paragraph on rebinding.
The headers also have, each as an item with its own *Constraints* and
*Remarks*:

- the converting constructors from `expected<U, G>` when `E` and `G` are
  both references, which take part only then and do not copy the error;
- the constructors and assignment operators from `unexpected<G>` when `E`
  and `G` are both references, which are `noexcept`;
- the same from `unexpected<G>` for a non-reference `G`, defined as deleted,
  because the referent would be inside the source object;
- the `unexpect_t` constructors defined as deleted when the argument would
  bind `E&` to a temporary, or is an initializer list.

Merging them now would take all of that out of the generated wording and
leave it nowhere but in comments. Leaving them is why `[expected.object.cons]`
has 15 items against the paper's 10, `[expected.object.assign]` 8 against 6,
`[expected.void.cons]` 13 against 8 and `[expected.void.assign]` 6 against 4.
Changing what the paper proposes is outside this plan, so the question is
recorded here and the overloads stay as they are until it is answered.
`[expected.ref]` is a different case: there the paper is shorter than the
headers by design, deferring to the primary template, and that belongs to
[converge-with-paper](#converge-with-paper).
**Log.**
- 2026-11-19: opened, in carrying out [synopsis-shape](#synopsis-shape).

### specgen-pin

**Question.** How is the specgen version fixed and recorded?
**Status.** DEFERRED
**Why.** specgen is moving to PyPI and will run through `uv`. The workflow,
the availability test in the makefile, and the pin are revisited then.
**Decided by.** Steve Downey, 2026-11-16.
**Log.**
- 2026-11-16: deferred.
- 2026-11-16: specgen went from 0.23.0 to 0.41.1 within the day, and the
  render changed with it. [regenerate](#regenerate) names the version it
  used in its commit message until there is a pin.
- 2026-11-17: 0.42.3 installed. Same plain render; only the draft import
  changed.
- 2026-11-19: 0.47.0 installed. The render changed in 42 lines, and the exit
  status changed: a specgen from 0.44.0 on fails `make wording` on the
  headers on `main`, where an older one succeeds. The cost of having no pin
  is now a build that works or not by which specgen is on `PATH`.

## Requests to specgen

Filed 2026-11-16, each with a scratch-header reproduction. All closed the
same day, and each reproduction rerun against 0.41.1.

| Request | Issue | Fixed in | For |
|---|---|---|---|
| Synopsis comments are dropped unless marked, those of an `\omit`ted member included | [specgen#280](https://github.com/steve-downey/specgen/issues/280) | `166c598` | [implementation-comments](#implementation-comments) |
| The synopsis drops a `requires`-clause that the item declaration states as *Constraints* | [specgen#281](https://github.com/steve-downey/specgen/issues/281) | `7f0f03f` | [synopsis-source](#synopsis-source) |
| A deleted tail spelled by a macro renders as `= delete` | [specgen#282](https://github.com/steve-downey/specgen/issues/282) | `5457c5e` | [deleted-message-spelling](#deleted-message-spelling) |
| Authored prose can stand for a class's derived ill-formed paragraph | [specgen#283](https://github.com/steve-downey/specgen/issues/283) | `41f6364` | [class-ill-formed-paragraph](#class-ill-formed-paragraph) |
| A detached `\verbatim-synopsis` in a `.syn` section is not wrapped again, and `/// END` closes the section | [specgen#284](https://github.com/steve-downey/specgen/issues/284) | `efc326e` | [header-synopsis-form](#header-synopsis-form) |
| A warning is what specgen verified; a note is what has to be checked outside it | [specgen#285](https://github.com/steve-downey/specgen/issues/285) | `0a849f6` | [warning-gate](#warning-gate) |
| An exposition-only name in an authored code span renders under its exposition name | [specgen#286](https://github.com/steve-downey/specgen/issues/286) | `31f75a4` | [exposition-names](#exposition-names) |

Filed 2026-11-18, from the 0.41.1 and 0.42.3 runs. All closed, and each
rerun on these headers with 0.47.0:

| Issue | What | Fixed in | Here |
|---|---|---|---|
| [specgen#348](https://github.com/steve-downey/specgen/issues/348) | A docblock above a definition whose first token is a macro is detached, or its item moves ahead of the class synopsis | 0.45.4 | the constructor of `[expected.bad]` stays with its class when the macro is `constexpr`; the `what()` that still leads the clause is the `<void>` one, a routing matter |
| [specgen#349](https://github.com/steve-downey/specgen/issues/349) | A macro standing for `constexpr` is written into the synopsis under its own name | 0.45.3 | works on a reduced header; not on this one, see below |
| [specgen#350](https://github.com/steve-downey/specgen/issues/350) | A docblock error does not change the exit status | 0.44.0 | exits 1 on the 7 errors |
| [specgen#351](https://github.com/steve-downey/specgen/issues/351) | The LaTeX backend writes a section title as its source text | 0.45.2 | backticked titles render `\tcode{...}` |
| [specgen#352](https://github.com/steve-downey/specgen/issues/352) | `&`, `%` and `#` in docblock prose are written to the LaTeX as they stand | 0.45.1 | the headers have none |
| [specgen#353](https://github.com/steve-downey/specgen/issues/353) | The exposition-only comment is written `// exposition only` | 0.44.1 | 14 lines now `// \expos` |
| [specgen#354](https://github.com/steve-downey/specgen/issues/354) | In a `--baseline-draft` diff, `\libglobal{name}` on a class head reads as a change | 0.44.2 | no mark on the class heads |
| [specgen#355](https://github.com/steve-downey/specgen/issues/355) | The importer keeps `\impldef`, `\ntbs`, `\term`, `\Fundescx`, `floattable`, and a list item holding a code block as raw LaTeX | 0.46.0, in part | 4 warnings left, carried by [specgen#367](https://github.com/steve-downey/specgen/issues/367), open |

Found 2026-11-19, and filed the same day:

| Issue | What | For |
|---|---|---|
| [specgen#377](https://github.com/steve-downey/specgen/issues/377) | A specifier macro that the header `#undef`s after its last use is printed under its own name, where the same macro left defined is written as its expansion. The expansion wanted is the one in effect where the macro is used. Reproduction below. | [macro-specifiers](#macro-specifiers) |
| [specgen#378](https://github.com/steve-downey/specgen/issues/378) | `--apply-to-draft` writes tokens added ahead of an access specifier on that specifier's line, so a `// \expos` comment among them swallows it; and on `expected.hpp` the run ends with `an edit of bytes N to N overlaps another or runs past the end` and writes no file. Related to [specgen#346](https://github.com/steve-downey/specgen/issues/346), open for placing an added subclause. | [draft-pull-request](#draft-pull-request) |

Filed 2026-11-19, from [synopsis-shape](#synopsis-shape):

| Issue | What | For |
|---|---|---|
| [specgen#383](https://github.com/steve-downey/specgen/issues/383) | Section prose written ahead of a section's first item is rendered after its items. | `[expected.ref.assign]`, and [class-prose](#class-prose) |
| [specgen#384](https://github.com/steve-downey/specgen/issues/384) | A deduction guide after its class is left out of the class synopsis, without a message. | [synopsis-shape](#synopsis-shape) |
| [specgen#385](https://github.com/steve-downey/specgen/issues/385) | No markup leaves out of the wording what an implementation declares beyond the standard: a strengthened `noexcept`, `= default`, a parameter name. | [implementation-extras](#implementation-extras) |
| [specgen#386](https://github.com/steve-downey/specgen/issues/386) | An empty `\constraints` removes the derived element, which the guide does not say; and a *Remarks* cannot cover a derived conjunct. | [overload-partitions](#overload-partitions), [validation-findings](#validation-findings) |

Not filed: a set of Doxygen `ALIASES` for specgen's markers, until
[api-site-markup](#api-site-markup) has one that works here.

The reproduction for the first. With `-DUSE_CX` the synopsis reads
`DEMO_CX const char* what() const noexcept;`. Without the `#undef` line it
reads `constexpr const char* what() const noexcept;`.

```cpp
#ifdef USE_CX
    #define DEMO_CX constexpr
#else
    #define DEMO_CX
#endif
namespace demo {
// \rSec2[demo.thing]{Thing}
class thing {
  public:
    DEMO_CX const char* what() const noexcept;
};

//! \returns A string.
inline DEMO_CX const char* thing::what() const noexcept { return "x"; }
} // namespace demo
#undef DEMO_CX
```

Not filed, and not needed: `\merge` recognizing a distinguishing conjunct
written `!(A && B)`. The defaulted twins here are unconstrained on purpose,
so there is no `A && B` on the twin for it to match.

## Files touched

- `include/beman/expected/{unexpected,bad_expected_access,expected}.hpp`:
  markup and comments only. No stage changes a declaration's meaning; a stage
  that would is a finding, recorded in the decision's log.
- `papers/wording/`: regenerated by every stage.
- `Makefile`, `papers/Makefile`: [regenerate](#regenerate) for the gate,
  [gap-yardstick](#gap-yardstick),
  [macro-expansion-args](#macro-expansion-args),
  [front-matter](#front-matter), [generated-diff](#generated-diff),
  [draft-edit](#draft-edit).
- `docs/Doxyfile`: [api-site](#api-site).
- `papers/wording/README.md`: its claim that `[expected.general]` and
  `[expected.syn]` cannot be generated goes with
  [front-matter](#front-matter).
- `papers/expected-new.tex`, `expected-base.tex`, `strip-wording.py`:
  retired by [generated-diff](#generated-diff).

## Out of scope

- The specgen installation and pin: [specgen-pin](#specgen-pin).
- Any change to what the paper proposes, `has_error()` included. Where the
  headers, the paper and the draft disagree, the disagreement is recorded and
  settled on its own.
- The `mpark` and `org` backends. The paper is LaTeX.
- Replacing Doxygen for the API site.
  [api-site-markup](#api-site-markup) makes it read the docblocks and goes no
  further.
- `split_inline`. The headers already declare in the class and define out of
  line, except `unexpected`, whose in-class definitions specgen reduces to
  declarations.
