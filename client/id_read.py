import os
import csv
import random

STANDARD_ID = 'X'*43
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def read_csv(filename):
    """
    This function allows to scan csv file and to get an id from the database.

    Args:
        filename (string): path to the csv file

    Returns:
        [string]: id read from database
    """

    with open(ROOT_DIR+filename) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for row in csvreader:
            if row[0] != STANDARD_ID:
                id_selected = row[0]
                break

    return id_selected