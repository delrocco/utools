import argparse
import os
import sys
import csv

def main():
    # handle command line args
    parser = argparse.ArgumentParser(description='Script to return complement of two lists.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('fname', help='a CSV of of 2 columns of info')
    args = parser.parse_args()

    # dir not found
    if not os.path.exists(args.fname):
        print("Error: no file found: '" + args.fname + "'")
        sys.exit(2)

    listA = []
    listB = []

    # read file
    with open(args.fname) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader) # skip header
        for row in reader:
            if not row: continue;
            if row[0] and len(row[0]) > 0:
                listA.append(row[0].lower())
            if row[1] and len(row[1]) > 0:
                listB.append(row[1].lower())

    print(*listA, sep='\n')
    print()
    print(*listB, sep='\n')
    print()

    listC = list(set(listA) - set(listB))
    listC = sorted(listC, key=str.lower)
    print(*listC, sep='\n')

if __name__ == "__main__":
    main()