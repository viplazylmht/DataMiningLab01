#!/usr/bin/env python3
import argparse
import csv
from math import floor
from list_missing import list_missing_column, getColumn

def mode(lst):
    return max(set(lst), key=lst.count)

def median(lst):
    # https://www.geeksforgeeks.org/python-statistics-median/
    l = sorted(lst)
    size = len(l)

    x1 = l[floor(size/2)]
    x2 = l[floor(size/2 + 0.5)]

    return (x1 + x2) / 2

def mean(lst):
    return sum(lst) / len(lst)


def evaluateColumnType(listRow, key):
    """
    Predict the type of column (numerical or categorical)
    """
    res = "numerical"

    # get a column without missing val
    l = [val for val in getColumn(listRow, key) if val != ""]

    if (len(l) == 0):
        res = "empty"
    else:
        try:
            for val in l:
                float(val)

            res = "numerical"
            pass
        except ValueError:
            res = "categorical"
            pass
    
    return res

def evaluateColumnTypeV2(valColumn):
    """
    Predict the type of column (numerical or categorical)
    """
    res = "numerical"

    # get a column without missing val
    l = [val for val in valColumn if val != ""]

    if (len(l) == 0):
        res = "empty"
    else:
        try:
            for val in l:
                float(val)

            res = "numerical"
            pass
        except ValueError:
            res = "categorical"
            pass
    
    return res

def get_fill_value(valColumn, method):
    
    m = evaluateColumnTypeV2(valColumn)
    res = ""

    if (m == 'empty'):
        # how to fill a col if this already empty?
        return res
    
    if (method == "auto"):
        if (m == "numerical"):
            method = "mean"
        if (m == "categorical"):
            method = "mode"
        
    if (method == "mean" and m == "numerical"):
        # get a column without missing val
        # then convert to float
        l = [float(val) for val in valColumn if val != ""]
        res = str(mean(l))

    if (method == "median" and m == "numerical"):
        # get a column without missing val
        # then convert to float
        l = [float(val) for val in valColumn if val != ""]
        res = str(median(l))

    # mode also compatible with both numerical or categorical
    if (method == "mode"):
        # get a column without missing val
        l = [val for val in valColumn if val != ""]
        res = str(mode(l))

    return res

def write_file(filename, listRow):
    with open(filename,'w', newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout)
        keys = [k for k in listRow[0].keys()]
        #print(keys)
        writer.writerows([keys])
    
        for json in listRow:
            row=[s for s in json.values()]
            #print(row)
            writer.writerows([row])

def fill_missing_column(filename, column, method="auto", fout="result.csv"):
    """
    Function to fill missings value each file with specified columns
    """

    listRow = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        listRow = [row for row in reader]

    if (column == None or len(column) == 0):
        # reassign column with all missing col
        column = list_missing_column(filename)

    keys = [key for key in listRow[0].keys()]

    print("{:20s}{:20s}{}".format("Column key", "Attr Type", "Fill value"))
    print("{:20s}{:20s}{}".format("----------", "---------", "----------"))
    for key in column:
        if (key not in keys):
            continue
        
        l = getColumn(listRow, key)
        fill = get_fill_value(l, method)

        for row in listRow:
            if row[key] == "":
                row[key] = fill

        print("{:20s}{:20s}{}".format(key, evaluateColumnTypeV2(l), fill))

    write_file(fout, listRow)
    print("\nSaved to {}".format(fout))
    pass

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Fill missing values to datas by a specified strategy')
    parser.add_argument('files_in', metavar='file', type=str, help='path to a csv file')
    parser.add_argument('--column',  metavar='column', type=str, nargs='+', 
                   help='title of columns\'s want to fill, if it was not specified, all column will be executed')
    parser.add_argument('--method',  action="store", default="auto", dest="method",
                   help='a strategy to fill out the value (accept {mean, median, mode, auto}, default is auto)')
    parser.add_argument('--out',  action="store", default="result.csv", dest="out",
                   help='output file name (default is result.csv)')

    args = parser.parse_args()

    #print(args)
    fill_missing_column(args.files_in, args.column, args.method, args.out)


