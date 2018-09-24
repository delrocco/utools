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
# @summary: Script to find and delete other exposures of HDR capture.
# ====================================================================
import sys
import os
import argparse


def main():
    # handle command line args
    parser = argparse.ArgumentParser(description='Script to find and delete other exposures of HDR capture. Assumes files sorted by exposure already!', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('directory', help='directory to search')
    parser.add_argument('-r', '--readonly', dest='readonly', action='store_true', help='read only mode (no writes)', default=False)
    parser.add_argument('-n', '--count', dest='count', type=int, help='number of exposures per capture (def = 8)', default=8)
    parser.add_argument('-k', '--keep', dest='keep', type=int, help='which exposure to keep (def = 1)', default=1)
    args = parser.parse_args()

    # valid dir required
    if not os.path.exists(args.directory):
        print("Error: directory not found: '" + args.directory + "'")
        sys.exit(2)

    # valid exposure required
    if args.keep < 0:
        print("Error: exposure must be positive (1 - count)")
        sys.exit(2)

    # walk dirs
    for root, dirs, files in os.walk(args.directory):
        exposures = []
        # find photos
        for f in files:
            fullpath = os.path.join(root, f)
            base, ext = os.path.splitext(fullpath.strip().lower())
            if ext == ".jpg":
                exposures.append(fullpath)
        # remove exposures we are not interested in
        if len(exposures) >= args.keep:
            if len(exposures) != args.count:  # if exposure count is different, I want to know, and not do anything yet
                print("Warning: " + str(len(exposures)) + " exposures in " + root)
            else:
                del exposures[args.keep-1]  # we only want to keep the exposure specified
                for e in exposures:  # remove the rest
                    print("Deleting: " + e)
                    if not args.readonly:
                        os.unlink(e)


if __name__ == "__main__":
    main()