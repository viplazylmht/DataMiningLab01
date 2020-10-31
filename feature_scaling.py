#!/usr/bin/env python3
import argparse
import csv
import statistics as stat
from math import floor
from list_missing import list_missing_column, getColumn
from impute import evaluateColumnType, evaluateColumnTypeV2, write_file

def normalize_column(filename, column, method="minmax", fout="result.csv"):
    """
    Function to normalize dataset with the specified columns
    """

    listRow = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        listRow = [row for row in reader]

    if (column == None or len(column) == 0):
        # Get all the columns with the type data is numberical in data set
        column = [key for key in listRow[0].keys(
        ) if evaluateColumnType(listRow, key) == 'numerical']

    keys = [key for key in listRow[0].keys()]

    print("{:20s}{:20s}{}".format("Column key", "Attr Type", "Status"))
    print("{:20s}{:20s}{}".format("----------", "---------", "------"))

    for key in column:
        if (key not in keys):
            print("{:20s}{:20s}{}".format(key, "NaN", "Not Found"))
            continue

        l = getColumn(listRow, key)

        typ = evaluateColumnTypeV2(l)

        # skip columns that are non-numeric values type
        if (typ != "numerical"):
            print("{:20s}{:20s}{}".format(key, typ, "Skipped"))
            continue

        # get a column without missing value and convert into number
        lst = [float(val) for val in l if val != ""]

        # follow this link for more details:
        # https://en.wikipedia.org/wiki/Feature_scaling

        # Rescaling (min-max normalization)
        if (method == "minmax"):
            minx = min(lst)
            maxx = max(lst)

            a = 0
            b = 1

            for row in listRow:
                if row[key] != "":
                    if (maxx == minx):
                        # fix division by 0 while min == max (all val equal together)
                        row[key] = str(0)
                    else:
                        row[key] = str(a + (float(row[key]) - minx)*(b - a) / (maxx - minx))
            
            print("{:20s}{:20s}{}".format(key, typ, "Done"))

        # Standardization (Z-score normalization)
        elif (method == "zscore"):
            mean = stat.mean(lst)
            deviation = stat.stdev(lst)

            for row in listRow:
                if row[key] != "":
                    if (deviation == 0):
                        # fix division by 0 while min == max (all val equal together)
                        row[key] = str(0)
                    else:
                        row[key] = str((float(row[key]) - mean) / deviation)

            print("{:20s}{:20s}{}".format(key, typ, "Done"))

        else:
            print("{:20s}{:20s}{}".format(key, typ, "Error"))

    write_file(fout, listRow)
    print("\nSaved to {}".format(fout))
    pass


if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(
        description='Normalizing column values of a dataset by a specified method')
    parser.add_argument('files_in', metavar='file',
                        type=str, help='path to a csv file')
    parser.add_argument('--column',  metavar='column', type=str, nargs='+',
                        help='title of columns\'s want to scaling, if it was not specified, all numeric column will be normalized')
    parser.add_argument('--method',  action="store", default="minmax", dest="method",
                        help='a method to normalize the value (accept {minmax, zscore}, default is minmax)')
    parser.add_argument('--out',  action="store", default="result.csv", dest="out",
                        help='output file name (default is result.csv)')

    args = parser.parse_args()

    #print(args)
    normalize_column(args.files_in, args.column, args.method, args.out)
