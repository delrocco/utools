#!/usr/bin/env python
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
# @since: 05/16/2018
# @summary: Script to swap 2 columns of a .csv file.
# ====================================================================
import os, sys
import argparse
import pandas as pd


def main():
    # handle command line args
    parser = argparse.ArgumentParser(description='Script to swap 2 columns of a .csv file. Use -r (--readonly) flag to preview changes first.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('file', help='csv file to operate on')
    parser.add_argument('colA', help='column A')
    parser.add_argument('colB', help='column B')
    parser.add_argument('-r', '--readonly', dest='readonly', action='store_true', help='read only mode (no writes)', default=False)
    args = parser.parse_args()

    # valid dir required
    if not os.path.exists(args.file):
        print("Error: file not found: '" + args.file + "'")
        sys.exit(2)

    # valid columns required
    args.colA = args.colA.strip()
    args.colB = args.colB.strip()
    if len(args.colA) <= 0 or len(args.colB) <= 0:
        print("Error: invalid column names: " + args.colA + ", " + args.colB)
        sys.exit(2)

    # read file
    df = pd.read_csv(args.file)

    print("Swapping cols: " + args.colA + " and " + args.colB)
    cols = list(df)
    mapping = {cols[i]: i for i in range(0, len(cols))}
    cols[mapping[args.colA]], cols[mapping[args.colB]] = cols[mapping[args.colB]], cols[mapping[args.colA]]
    df = df.reindex(columns=cols)

    # write new file
    if not args.readonly:
        fname, ext = os.path.splitext(args.file)
        df.to_csv(fname + "_new" + ext, sep=',', index=False)

if __name__ == "__main__":
    main()
