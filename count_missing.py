#!/usr/bin/env python3
import argparse
import csv
from list_missing import list_missing_column

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Count columns that missing values')
    parser.add_argument('files_in', metavar='file', type=str, nargs='+',
                   help='paths to csv file')

    args = parser.parse_args()

    #print(args)
    for f in args.files_in:
        if (len(args.files_in) > 1):
            print("In file %s: " % f)
        print(len(list_missing_column(f, False)))
      