import os
import csv

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def read_csv(csv_path, read_valid_id):
    """
    This function allows to read csv file and to get an id from the database.

    Args:
        csv_path (string): the path of csv file to read
        read_valid_id (bool): it is True or False to indicates if we want an id valid or not
        
    Returns:
        [string]: id read from database
    """
    with open(ROOT_DIR+csv_path) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ')
        if read_valid_id:
            (next(csvreader))
        else:
            for i in range(0,11):
                (next(csvreader))

        for row in csvreader:
            split = row[0].split(",")
            id_name = split[0]
            break
        return id_name