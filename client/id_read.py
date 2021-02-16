import os
import csv
import random

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
filename= ROOT_DIR + "/../authorityServer/database.csv"

def read_random_lines():
    """
    This function allows to scan csv file and to get a random id from the database.

    Returns:
        [string]: id read from database
    """
    lines = list()

    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for row in csvreader:
            lines.append(row[0])
        
        id_selected = random.choice(lines)

    return id_selected