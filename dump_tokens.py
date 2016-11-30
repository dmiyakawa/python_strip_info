#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ref. http://stackoverflow.com/questions/1769332/
#

from io import BytesIO
import sys
import tokenize
from tokenize import tok_name


def dump_tokens(source: bytes) -> str:
    io_obj = BytesIO(source)
    for tok in tokenize.tokenize(io_obj.readline):
        tok_type = tok[0]
        tok_string = tok[1]
        # start_line, start_col = tok[2]
        # end_line, end_col = tok[3]
        # line = tok[4]
        print('{} {!r}'.format(tok_name[tok_type], tok_string))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        filenames = [__file__]
    for filename in filenames:
        print(dump_tokens(open(filename, 'rb').read()))
