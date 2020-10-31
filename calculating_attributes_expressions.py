#!/usr/bin/env python3
import argparse
import csv
from math import floor
from impute import evaluateColumnType, write_file

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def isopt(value):
    return value in ["+", "-", "*", "/"]

def calculating_attributes_expressions(filename, exprs, cname='new', fout="result.csv"):
    """
    Function to calculate the value of an attribute expressions
    Append new attribute to end of dataset
    """

    listRow = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        listRow = [row for row in reader]

    keys = [key for key in listRow[0].keys()]

    # checkout vaild expression
    last = ""
    for expr in exprs:
        cur = "opt" if isopt(expr) else "number" if isfloat(expr) else "none"

        if cur == "none":
            if expr not in keys:
                print("ERROR: Expression syntax not allowed")
                print("at: {}: attr not found".format(expr))
                exit(1)

            if evaluateColumnType(listRow, expr) != "numerical":
                print("ERROR: Expression syntax not allowed")
                print("at: {}: Expected a numeric attr".format(expr))
                exit(1)

        if (cur == last):
            print("ERROR: Expression syntax not allowed")
            print("at: {}".format(expr))
            exit(1)

        last = cur
    
    # calculating
    for row in listRow:

        param = []
        flag = True

        for expr in exprs:
            if (not isopt(expr) and not isfloat(expr)):
                if (row[expr] == ""):
                    flag = False
                    break 

                param.append(row[expr])
            else:
                param.append(expr)
        # adding " " between parameters and caculating expressions with eval()
        if (flag == True):
            row[cname] = eval(" ".join(param))

    write_file(fout, listRow)
    print("Saved to {}".format(fout))
    pass


if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(
        description='Clustering columns values of a dataset by a specified expression')
    parser.add_argument('files_in', metavar='file',
                        type=str, help='path to a csv file')
    parser.add_argument('exprs', metavar='expressions', type=str, nargs='+',
                        help='expression (contain columns and also + - * / operator)')
    parser.add_argument('--cname',  action="store", default="new",
                        help='name of the new attribute')
    parser.add_argument('--out',  action="store", default="result.csv", dest="out",
                        help='output file name (default is result.csv)')

    args = parser.parse_args()

    #print(args)

    calculating_attributes_expressions(args.files_in, args.exprs, args.cname, args.out)
    