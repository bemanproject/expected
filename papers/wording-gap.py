#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Measure how far the generated [expected] wording is from two references.

    wording-gap.py tokens PAPER GENERATED
        PAPER is the paper's hand-marked wording with its change markup
        stripped (strip-wording.py), GENERATED is wording/expected.tex.
        Both are read from \\rSec2[expected.unexpected] to the end and
        split into code -- the lines of a codeblock or an itemdecl, with
        the \\begin and \\end lines -- and prose, which is everything else.
        Each is counted in whitespace-separated tokens, because the paper
        wraps its prose by hand and specgen writes a paragraph on one line.
        "Only in" is what a minimal diff of the two token sequences leaves
        on that side.

    wording-gap.py marks PAPER_MARKED DIFF_DIR CLAUSE...
        PAPER_MARKED is the paper's wording as it is written, with its
        \\added and addedblock markup. DIFF_DIR holds one CLAUSE.tex per
        clause, the fragments of a specgen run with --baseline-draft. For
        each clause, counts the change marks specgen made against the
        working draft and the ones the paper makes by hand.

Neither command fails on what it finds: these are yardsticks, not gates.
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FIRST_CLAUSE = '\\rSec2[expected.unexpected]'
CODE_BEGIN = re.compile(r'\\begin\{(codeblock|itemdecl)\}')
CODE_END = re.compile(r'\\end\{(codeblock|itemdecl)\}')


def tokens(path):
    """Return (code, prose) token lists for the wording in path."""
    code, prose = [], []
    in_code = False
    started = False
    for line in Path(path).read_text().splitlines():
        if not started:
            if not line.startswith(FIRST_CLAUSE):
                continue
            started = True
        if CODE_BEGIN.match(line):
            in_code = True
            code.extend(line.split())
        elif CODE_END.match(line):
            in_code = False
            code.extend(line.split())
        else:
            (code if in_code else prose).extend(line.split())
    return code, prose


def only_in(left, right):
    """Tokens a minimal diff leaves on each side: (only_left, only_right)."""
    with tempfile.TemporaryDirectory() as tmp:
        a, b = Path(tmp, 'a'), Path(tmp, 'b')
        a.write_text('\n'.join(left) + '\n')
        b.write_text('\n'.join(right) + '\n')
        # diff exits 1 when the files differ, which is the expected case.
        out = subprocess.run(['diff', '--minimal', a, b],
                             capture_output=True, text=True).stdout
    lines = out.splitlines()
    return (sum(1 for line in lines if line.startswith('<')),
            sum(1 for line in lines if line.startswith('>')))


def cmd_tokens(args):
    paper_code, paper_prose = tokens(args.paper)
    gen_code, gen_prose = tokens(args.generated)
    print('Tokens, generated wording against the paper\'s:')
    print(f'  {"":8}{"paper":>8}{"generated":>11}'
          f'{"only paper":>12}{"only generated":>16}')
    for name, paper, gen in (('code', paper_code, gen_code),
                             ('prose', paper_prose, gen_prose)):
        only_paper, only_gen = only_in(paper, gen)
        print(f'  {name:8}{len(paper):>8}{len(gen):>11}'
              f'{only_paper:>12}{only_gen:>16}')


def clause_text(marked, clause):
    """The text of one \\rSec2 clause of the paper's marked wording."""
    lines = Path(marked).read_text().splitlines()
    out = []
    inside = False
    for i, line in enumerate(lines):
        if line.startswith('\\rSec2['):
            inside = line.startswith(f'\\rSec2[{clause}]')
            # A clause that is new as a whole is wrapped in a block that
            # opens on the lines before its heading. That block is this
            # clause's, not the one before's.
            opening = []
            j = i - 1
            while j >= 0 and lines[j].strip() in ('', '\\begin{addedblock}'):
                opening.append(lines[j])
                j -= 1
            if inside:
                out.extend(reversed(opening))
            else:
                del out[len(out) - min(len(out), len(opening)):]
        if inside:
            out.append(line)
    return '\n'.join(out)


def count_marks(text):
    return (text.count('\\added{'), text.count('\\removed{'),
            text.count('\\begin{addedblock}'),
            text.count('\\begin{removedblock}'))


def cmd_marks(args):
    print('Change marks against the working draft '
          '(inline added / removed, blocks added / removed):')
    print(f'  {"clause":24}{"generated":>22}{"paper":>22}')
    for clause in args.clauses:
        fragment = Path(args.diff_dir, clause + '.tex')
        if fragment.exists():
            a, r, ab, rb = count_marks(fragment.read_text())
            generated = f'{a} / {r}, {ab} / {rb}'
        else:
            generated = 'not written'
        a, r, ab, rb = count_marks(clause_text(args.paper_marked, clause))
        paper = f'{a} / {r}, {ab} / {rb}'
        print(f'  {clause:24}{generated:>22}{paper:>22}')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('tokens')
    p.add_argument('paper')
    p.add_argument('generated')
    p.set_defaults(func=cmd_tokens)
    p = sub.add_parser('marks')
    p.add_argument('paper_marked')
    p.add_argument('diff_dir')
    p.add_argument('clauses', nargs='+')
    p.set_defaults(func=cmd_marks)
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
