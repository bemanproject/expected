#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Doxygen input filter for headers whose docblocks are written for specgen.

The `//!` docblocks in include/beman/expected/ are the source of the paper's
wording, which specgen generates from them. Doxygen reads `//!` as its own
comment form and builds the API site from the same text, but it does not know
specgen's markers. docs/Doxyfile handles the element tags that take a
paragraph (`\\effects`, `\\constraints`, ...) with ALIASES. This filter handles
what an alias cannot:

  * A marker that takes the rest of its line as an argument, or none, and
    says something about the wording and nothing to a reader of the API:
    `\\at stable.name`, `\\group id`, `\\covers mandates P`,
    `\\seebelow noexcept`, `\\merge`, and the like. The line is blanked.
  * `\\also`, which joins an overload to the item described before it. It
    becomes Doxygen's `\\overload`, which says the same thing to a reader.
  * `\\verbatim-synopsis`, after which the rest of the docblock is the
    synopsis as the standard prints it. Those lines become plain comments,
    which Doxygen does not read.
  * The working draft's inline macros with a braced argument, which may nest
    and may hold commas: `\\tcode{x}`, `\\iref{x}`, `\\ref{x}`, `\\tref{x}`,
    `\\term{x}`, `\\oldconcept{X}`, `\\Fundescx{X}`, `\\impldef{x}`, `\\ntbs{}`,
    `\\cv{}`. Each is rewritten to plain Doxygen text.

Every line of input produces one line of output, so the line numbers in
Doxygen's messages and in the generated pages are the header's own.

Usage, as Doxygen calls it: specgen-doxygen-filter.py <header>
"""

import re
import sys

# Markers that are a whole line by themselves or with their argument.
LINE_MARKERS = (
    'at', 'group', 'covers', 'seebelow', 'expos', 'merge', 'omit',
    'elsewhere', 'describe', 'freestanding', 'freestanding-deleted',
    'constraints-in-decl', 'synopsis-here', 'asdraft', 'asdraft-synopsis',
    'specified', 'impdef',
)
MARKER_LINE = re.compile(
    r'^(\s*//!)\s*\\(' + '|'.join(re.escape(m) for m in LINE_MARKERS) +
    r')(?![\w-]).*$')
DOCBLOCK_LINE = re.compile(r'^(\s*)//!(.*)$')
ALSO_LINE = re.compile(r'^(\s*//!)\s*\\also(?![\w-]).*$')
VERBATIM = re.compile(r'^\s*//!\s*\\verbatim-(synopsis|itemdecl)\b')

# Inline macros: name -> how to write the (already rewritten) argument.
INLINE = {
    'tcode': lambda a: '<code>' + a + '</code>',
    'iref': lambda a: ' [' + a + ']',
    'ref': lambda a: '[' + a + ']',
    'tref': lambda a: '[' + a + ']',
    'term': lambda a: '<em>' + a + '</em>',
    'defn': lambda a: '<em>' + a + '</em>',
    'oldconcept': lambda a: '<em>Cpp17' + a + '</em>',
    'Fundescx': lambda a: '<em>' + a + '</em>',
    'impldef': lambda a: 'implementation-defined',
    'ntbs': lambda a: 'NTBS',
    'ntmbs': lambda a: 'NTMBS',
    'cv': lambda a: '<em>cv</em>',
    'libconcept': lambda a: '<code>' + a + '</code>',
    'exposconcept': lambda a: '<em>' + a + '</em>',
    'placeholder': lambda a: '<em>' + a + '</em>',
}
INLINE_START = re.compile(r'\\(' + '|'.join(INLINE) + r')\{')


def rewrite_inline(text):
    """Rewrite the braced inline macros in text, innermost first."""
    out = []
    i = 0
    while True:
        m = INLINE_START.search(text, i)
        if not m:
            out.append(text[i:])
            return ''.join(out)
        out.append(text[i:m.start()])
        depth = 1
        j = m.end()
        while j < len(text) and depth:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
            j += 1
        if depth:
            # The argument continues on the next line. Leave the line as it
            # is: a macro split across lines is rare, and guessing is worse.
            out.append(text[m.start():])
            return ''.join(out)
        out.append(INLINE[m.group(1)](rewrite_inline(text[m.end():j - 1])))
        i = j


def filter_lines(lines):
    in_verbatim = False
    for line in lines:
        ending = '\n' if line.endswith('\n') else ''
        body = line[:-1] if ending else line
        doc = DOCBLOCK_LINE.match(body)
        if not doc:
            in_verbatim = False
            yield line
            continue
        if in_verbatim or VERBATIM.match(body):
            in_verbatim = True
            yield doc.group(1) + '//' + doc.group(2) + ending
            continue
        also = ALSO_LINE.match(body)
        if also:
            yield also.group(1) + ' \\overload' + ending
            continue
        marker = MARKER_LINE.match(body)
        if marker:
            yield marker.group(1) + ending
            continue
        yield doc.group(1) + '//!' + rewrite_inline(doc.group(2)) + ending


def main():
    if len(sys.argv) != 2:
        sys.stderr.write(__doc__)
        return 2
    with open(sys.argv[1], encoding='utf-8') as f:
        sys.stdout.writelines(filter_lines(f))
    return 0


if __name__ == '__main__':
    sys.exit(main())
