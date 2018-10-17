#!/usr/bin/python
# -*- coding: utf-8 -*-
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