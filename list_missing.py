#!/usr/bin/env python3
import argparse
import csv

def getColumn(listRow, key):
    """
    Get a list of value by a specified key
    - listRow: a list of dict
    - key: string 
    return a list of column
    """
    res = [row[key] for row in listRow]
    return res

def getMissingRate(listRow, key):
    """
    Get missing rate of a specified key
    - listRow: a list of dict
    - key: string 
    return rate (0 <= rate <= 1)
    """
    num = getColumn(listRow, key).count("")
    return 0 if (len(listRow) == 0) else num / len(listRow)


def list_missing_column(filename, extra=False):
    """
    Function to list missing value each file 
    return an array of string line instead of print out all line to console
    """
    res = []
    listRow = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        listRow = [row for row in reader]

    l = {key: getColumn(listRow, key).count("") for key in listRow[0].keys()}
    rowCount = len(listRow)

    if (extra == False):
        for key in l.keys():
            if (l[key] > 0):
                # only export this key
                #print(key)
                res.append(key)
    else:
        res.append("{:25s}{:25s}{}".format("Column key", "Missing rate (%)", "Count"))
        res.append("{:25s}{:25s}{}".format("----------", "----------------", "-----"))
        #print("{:25s}{:25s}{}".format("Column key", "Missing rate (%)", "Count"))
        #print("{:25s}{:25s}{}".format("----------", "----------------", "-----"))
        for key in l.keys():
            if (l[key] > 0):
                # getMissingRate in short hand
                res.append("{:25s}{:-10.2f}{:-20d}".format(key, l[key] / rowCount * 100, l[key]))
                #print("{:25s}{:-10.2f}{:-20d}".format(key, l[key] / rowCount * 100, l[key]))
    
    return res

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='List columns that missing values')
    parser.add_argument('files_in', metavar='file', type=str, nargs='+',
                   help='paths to csv file')
    parser.add_argument('--extra', action="store_true", default=False,
                   help='print out extra info about missing column')

    args = parser.parse_args()

    #print(args)
    for f in args.files_in:
        if (len(args.files_in) > 1):
            print("In file %s: " % f)
        print(*list_missing_column(f, args.extra), sep = "\n")
        
