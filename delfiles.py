#!/usr/bin/python
# -*- coding: utf-8 -*-
# ====================================================================
# Copyright (c) 2018 Joe Del Rocco
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ====================================================================
# @author: Joe Del Rocco
# @since: 9/21/2018
# @summary: Script to find and delete files of a specified extension.
# ====================================================================
import sys
import os
import argparse
import utility


def main():
    # handle command line args
    parser = argparse.ArgumentParser(description='Script to find and delete files of a specified extension. Use -r (--readonly) flag to preview changes first.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('directory', help='directory to search')
    parser.add_argument('extension', help='file extension to look for')
    parser.add_argument('-r', '--readonly', dest='readonly', action='store_true', help='read only mode (no writes)', default=False)
    parser.add_argument('-R', '--recursive', dest='recursive', action='store_true', help='recurse subdirs (def = true)', default=True)
    args = parser.parse_args()

    # valid dir required
    if not os.path.exists(args.directory):
        print("Error: directory not found: '" + args.directory + "'")
        sys.exit(2)

    # valid ext required
    args.extension = args.extension.strip()
    if len(args.extension) <= 0:
        print("Error: invalid extension")
        sys.exit(2)

    # do it
    files = utility.findFiles(args.directory, 1, args.recursive, [args.extension])
    for f in files:
        print("Deleting: " + f)
        if not args.readonly:
            os.unlink(f)

if __name__ == "__main__":
    main()