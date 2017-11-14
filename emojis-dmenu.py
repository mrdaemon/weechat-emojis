#!/usr/bin/env python
# Copyright (c) 2017 Oliver Uvman
#
# Some rights reserved.
#
# Redistribution and use in source and binary forms of the software as well
# as documentation, with or without modification, are permitted provided
# that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided
#   with the distribution.
#
# THIS SOFTWARE AND DOCUMENTATION IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE AND DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

import os
import sys

EMOJIS = {}


def load_emojis():
    """ Load emojis from file """

    global EMOJIS

    thisdir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(thisdir, "emojis-db.dat")

    with open(path) as f:
        for line in f:
            if line.startswith(':'):
                key = line.rstrip()
                val = f.next().rstrip()
                key = key[1:]
                key = key[:-1]
                EMOJIS[key] = val


def main():
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == '-h' or arg == '--help':
            print('No args: print keys and values, separated with spaces')
            print('One arg, line from no arg output, print associated value')
            return

    global EMOJIS
    try:
        load_emojis()
    except IOError as e:
        raise e  # aw dang

    if len(sys.argv) < 2:
        longest = len(max(EMOJIS.keys(), key=len))
        for k, v in EMOJIS.iteritems():
            spaces = 1 + longest - len(k)
            print(k + spaces * ' ' + EMOJIS[k])
        return

    if len(sys.argv) >= 2:
        # Yeah yeah, I know it should be done in bash
        print(EMOJIS[sys.argv[1].split(' ', 1)[0]])


if __name__ == '__main__':
    main()
