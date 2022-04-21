#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ====================================================================
# @author: Joe Del Rocco
# @since: 04/04/2022
# @summary: Script to generate report on rec directory of csv files.
# ====================================================================
import os
import sys
import io
#import shutil
#import asyncio
from concurrent.futures import ProcessPoolExecutor
import argparse
import operator
import csv
from datetime import date


# datafiles = "datafiles.csv"
# datafiles_prev = "datafiles_prev.csv"
# report = "report.csv"

# '''
# Helper function for concurrency that runs a separate thread for some job
# '''
# def background(f):
#     def wrapped(*args, **kwargs):
#         return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
#     return wrapped

'''
Helper function that returns a list of all files, directories, or both, immediate or recursive.
:param mode: 0=both, 1=files, 2=dir
:param recursive: Immediate top-level list or recursive list
:param ext: List of file extensions to filter by
'''
def findFiles(dirpath, mode=0, recursive=False, ext=[]):
    stuff = []
    if len(ext) > 0:
        for i in range(0, len(ext)):
            ext[i] = ext[i].strip().lower()
            if ext[i][0] != ".":
                ext[i] = "." + ext[i]
    # immediate top-level list
    if not recursive:
        for entry in os.listdir(dirpath):
            fullpath = os.path.join(dirpath, entry)
            if mode == 1 or mode == 0:
                base, extension = os.path.splitext(fullpath.strip().lower())
                if os.path.isfile(fullpath):
                    if len(ext) > 0:
                        for e in ext:
                            if extension == e:
                                stuff.append(fullpath)
                    else:
                        stuff.append(fullpath)
            if mode == 2 or mode == 0:
                if os.path.isdir(fullpath):
                    stuff.append(fullpath)
    # recursive list
    else:
        for root, dirs, files in os.walk(dirpath):
            if mode == 1 or mode == 0:
                for file in files:
                    fullpath = os.path.join(root, file)
                    base, extension = os.path.splitext(fullpath.strip().lower())
                    if len(ext) > 0:
                        for e in ext:
                            if extension == e:
                                stuff.append(fullpath)
                    else:
                        stuff.append(fullpath)
            if mode == 2 or mode == 0:
                for dir in dirs:
                    fullpath = os.path.join(root, dir)
                    stuff.append(fullpath)
    return stuff

'''
Function that actually reads and processes a single CSV file (on a separate thread).
:param args: argparse args for the program
:param csvfilepath: The filepath of the CSV file to process
:param results: List of results from processing the file
'''
#@background
def processCSVFile(csvfilepath):
    result = []
    with io.open(csvfilepath, mode="r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile) # , delimiter=delimiter
        columns = next(reader)
        numrows = sum(1 for line in reader)
        # new result row
        result = []
        result.append(csvfilepath)
        result.append(str(len(columns)))
        result.append(str(numrows))
    return result

def main():
    # handle command line args
    parser = argparse.ArgumentParser(description='Script to report on dir of CSV files', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('csv', help='directory of csv files that will be processed')
    parser.add_argument('out', help='full filepath of report')
    #parser.add_argument('-n', '--dim', dest='dim', type=int, nargs=2, default=(1024,768), help='dimensions as ints (def 1024 768)')
    #parser.add_argument('-c', '--columns', dest='columns', action='store_true', default=False, help='list the columns')
    #parser.add_argument('-nc', '--numcols', dest='numcols', action='store_true', default=False, help='get num columns')
    #parser.add_argument('-nr', '--numrows', dest='numrows', action='store_true', default=False, help='get num rows')
    # parser.add_argument('-q', '--quality', dest='quality', type=int, default=90, help='quality 1-95 (def 90)')
    parser.add_argument('-d', '--delimiter', dest='delimiter', type=str, default=',', help='delimiter character ("," " " "\\t")')
    args = parser.parse_args()

    # global datafiles
    # global datafiles_prev
    # global report

    # HARDCODED REQUEST: Windows folder path + current date (20220322)
    #args.csv = "\\\\jwbfilesvr1p\\JWBSFTPSHARE\\Amplifund\\Tables\\"
    today = date.today()
    todaystr = '{:4d}{:02d}{:02d}'.format(today.year, today.month, today.day)
    args.csv = os.path.join(args.csv, todaystr)

    print(args.csv)
    print(os.path.dirname(args.out))
    print(args.out)

    # csv dir not found
    if not os.path.exists(args.csv):
        print("ERROR: Input csv dir not found or can't access: '" + args.csv + "'")
        sys.exit(2)

    # out dir not found
    if not os.path.exists(os.path.dirname(args.csv)):
        print("ERROR: Report dir not found or can't access: '" + os.path.dirname(args.csv) + "'")
        sys.exit(2)

    # # current report not found
    # if not os.path.exists(datafiles):
    #     print("WARNING: No current report found in current working directory: '" + datafiles + "'")
    #     print("WARNING: Cannot compare current and previous report.")
    # else:
    #     shutil.copy(datafiles, datafiles_prev)

    # find all .csv files recursively
    print("Looking for csv in " + args.csv)
    csvfiles = findFiles(args.csv, 1, True, ['.csv'])
    print("Found " + str(len(csvfiles)) + " files")

    # iterate through them and process on separate processes (to utilize more CPU)
    results = []
    with ProcessPoolExecutor() as executor:
        for result in executor.map(processCSVFile, (csvfiles)):
            results.append(result)

    # sort report by filepath
    sorted(results, key=operator.itemgetter(0))

    # write report
    print("Writing report to " + args.out)
    with io.open(args.out, mode="w+", encoding="utf-8", newline='') as wfile:
        #reportfile = io.open(report, mode="w+", encoding="utf-8")
        writer = csv.writer(wfile, delimiter=args.delimiter)
        writer.writerow(["Filepath", "NumCols", "NumRows"])
        for row in results:
            writer.writerow(row)

    # # generate report between current and previous run
    # if os.path.exists(datafiles_prev):
    #     with io.open(report, mode="w+", encoding="utf-8", newline='') as wfile, io.open(datafiles, mode="r", encoding="utf-8") as rfile_curr, io.open(datafiles_prev, mode="r", encoding="utf-8") as rfile_prev:
    #         writer = csv.writer(wfile, delimiter=args.delimiter)
    #         writer.writerow(["Filepath", "NumColsCurr", "NumColsPrev", "Diff"])
    #
    #         # read current listing
    #         reader_curr = csv.reader(rfile_curr, delimiter=args.delimiter)
    #         curr = list(reader_curr)
    #
    #         # read previous listing
    #         reader_prev = csv.reader(rfile_prev, delimiter=args.delimiter)
    #         prev = list(reader_prev)
    #
    #         # report on each row of the current and previous datafile listings
    #         for i in range(1, len(curr)):
    #             writer.writerow([curr[i][0], curr[i][1], prev[i][1], int(curr[i][1])-int(prev[i][1])])

if __name__ == "__main__":
    main()
