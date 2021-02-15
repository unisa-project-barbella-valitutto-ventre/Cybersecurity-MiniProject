import os
import csv

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def read_csv(csv_path, read_valid_id):

    with open(ROOT_DIR+csv_path) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ')
        if read_valid_id:
            (next(csvreader))
        else:
            for i in range(0,5):
                (next(csvreader))

        for row in csvreader:
            split = row[0].split(",")
            id_name = split[0]
            break
        return id_name