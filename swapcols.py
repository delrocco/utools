#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
