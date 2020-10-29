#!/usr/bin/env python3
import argparse
import csv
from list_missing import list_missing_column, getColumn, getMissingRate
from impute import write_file

def remove_row_missing(listData, rate):
    """
    return new listData
    """
    res = []

    for row in listData:
        count = 0
        for val in row.values():
            count += 1 if val == "" else 0

        size = len(row)

        r = (0 if (size == 0) else count / size) * 100

        # only append valid row
        if r < rate:
            res.append(row)

    return res

def remove_col_missing(listData, rate):
    """
    return new listData
    """

    res = [row.copy() for row in listData]

    for key in listData[0].keys():
        r = getMissingRate(listData, key) * 100
        if (r >= rate):
            for row in res:
                # remove this key pair
                row.pop(key)

    return res

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(
        description='Remove missing column or row with a specified missing rate')
    parser.add_argument('files_in', metavar='file',
                        type=str, help='path to a csv file')
    parser.add_argument('miss_rate', metavar='rate', type=int,
                        help='minimum missing rate that will be removed')
    parser.add_argument('--column', action="store_true", default=False,
                        help='if it was not specified, remove row instead of column')
    parser.add_argument('--out',  action="store", default="result.csv", dest="out",
                        help='output file name (default is result.csv)')

    args = parser.parse_args()

    #print(args)
    
    rate = args.miss_rate
    fout = args.out

    filename = args.files_in

    listRow = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        listRow = [row for row in reader]

    if (args.column == True):
        listRow = remove_col_missing(listRow, rate)
    else:
        listRow = remove_row_missing(listRow, rate)

    write_file(fout, listRow)
