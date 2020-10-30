#!/usr/bin/env python3
import argparse
import csv

def count_missing_row(filename):
    """
    Function to list missing value each file 
    return an array of string line instead of print out all line to console
    """
    res = 0
    listRow = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        listRow = [row for row in reader]


    rowCount = len(listRow)
    if (rowCount == 0):
        return res

    for row in listRow:
        count = sum([1 for val in row.values() if val == ""])
        
        if count > 0:
            res += 1

    return res

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Count rows that missing values')
    parser.add_argument('files_in', metavar='file', type=str, nargs='+',
                   help='paths to csv file')

    args = parser.parse_args()

    #print(args)
    for f in args.files_in:
        if (len(args.files_in) > 1):
            print("In file %s: " % f)
        print(count_missing_row(f))
      