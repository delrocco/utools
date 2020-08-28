#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ====================================================================
# @author: Joe Del Rocco
# @since: 08/28/2020
# @summary: Script to rename GitHub Classroom repos with identifiers.
# ====================================================================
import os
import sys
import argparse
import csv
import utility

def main():
    # handle command line args
    parser = argparse.ArgumentParser(description='Script to rename GitHub Classroom repos to use student roster identifiers.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('directory', help='a directory of student repos')
    parser.add_argument('roster', help='a classroom roster file from GitHub')
    parser.add_argument('-r', '--readonly', dest='readonly', action='store_true', help='read only mode (no writes)', default=False)
    args = parser.parse_args()

    # dir not found
    if not os.path.exists(args.directory):
        print("Error: no directory found: '" + args.directory + "'")
        sys.exit(2)
    # roster not found
    if not os.path.exists(args.roster):
        print("Error: no file found: '" + args.roster + "'")
        sys.exit(2)

    # read the classroom roster file from GitHub Classroom
    username2identifier = {}
    with open(args.roster) as roster:
        reader = csv.DictReader(roster, delimiter=',')
        for row in reader:
            identifier = row['identifier']
            username = row['github_username']
            username2identifier[username] = identifier

    # do the renaming
    print("Renaming repos in: " + args.directory)
    dirs = utility.findFiles(args.directory, 2)
    for d in dirs:
        dirpath = os.path.dirname(d)
        username = os.path.basename(d)
        if username in username2identifier:
            print("Renaming: " + username + " -> " + username2identifier[username])
            if not args.readonly:
                dnew = os.path.join(dirpath, username2identifier[username])
                os.rename(d, dnew)

if __name__ == "__main__":
    main()