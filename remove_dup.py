#!/usr/bin/env python3
import argparse
import csv
from list_missing import list_missing_column, getColumn, getMissingRate
from impute import write_file


def remove_dup(listData):
    """
    return new listData
    """
    res = []

    for row in listData:
        
        # only append non duplicate row
        if row not in res:
            res.append(row.copy())

    return res

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(
        description='Remove duplicate rows appear in data set')
    parser.add_argument('files_in', metavar='file',
                        type=str, help='path to a csv file')
    parser.add_argument('--out',  action="store", default="result.csv", dest="out",
                        help='output file name (default is result.csv)')

    args = parser.parse_args()

    #print(args)
    
    fout = args.out

    filename = args.files_in

    listRow = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        listRow = [row for row in reader]

    
    listRow = remove_dup(listRow)
    
    write_file(fout, listRow)

