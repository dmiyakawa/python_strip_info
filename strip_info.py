#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on the code in
# http://stackoverflow.com/questions/1769332/
#

from io import BytesIO
import sys
import tokenize


def remove_info(source: bytes, use_untokenize: bool = False) -> str:
    """\
    ソースコードを受取り、docstring, コメントが含まれる。

    use_untokenizeがTrueの場合、tokenize.untokenize()を使用して
    ソースコードを再構築する。
    """
    io_obj = BytesIO(source)
    out = []
    all_tokens = []
    prev_tok_type = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.tokenize(io_obj.readline):
        tok_type = tok[0]
        tok_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        do_append = False
        if tok_type in {tokenize.COMMENT, tokenize.ENCODING}:
            pass
        elif tok_type == tokenize.NL and prev_tok_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif tok_type == tokenize.STRING:
            if prev_tok_type != tokenize.INDENT:
                # This is likely a docstring;
                # double-check we're not inside an operator:
                #
                # Note regarding NEWLINE vs NL:
                # The tokenize module differentiates between newlines
                # that start a new statement and newlines inside of
                # operators such as parens, brackes,
                # and curly braces.  Newlines inside of operators are
                # NEWLINE and newlines that start new code are NL.
                # Catch whole-module docstrings:
                if prev_tok_type != tokenize.NEWLINE:
                    if start_col > 0:
                        do_append = True

        else:
            do_append = True

        if do_append:
            if not use_untokenize:
                # tokenize.untokenize()を使用しない場合、
                # インデントに関する情報を手動で復元するする必要がある。
                if start_line > last_lineno:
                    last_col = 0
                if start_col > last_col:
                    out.append(' ' * (start_col - last_col))
            if use_untokenize:
                out.append(tok)
            else:
                out.append(tok_string)

        prev_tok_type = tok_type
        last_col = end_col
        last_lineno = end_line
        all_tokens.append(tok)
    if use_untokenize:
        return tokenize.untokenize(out)
    else:
        return ''.join(out)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        filenames = [__file__]
    for filename in filenames:
        print(remove_info(open(filename, 'rb').read()))
