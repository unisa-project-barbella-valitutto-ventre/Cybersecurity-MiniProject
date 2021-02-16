import secrets
import datetime
import csv
import random
import utils

fields = ['id', 'cod_device', 'id_time', 'cod_time']
filename = "database.csv"

def shuffle_database():
    """
    Function to shuffle the database
    """
    lines = list()
    with open(filename, 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
                lines.append(row)

    random.shuffle(lines)

    with open(filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(fields)
        writer.writerows(lines)


if __name__ == "__main__":
    """
    Function to populate database in order to test the simulation:
        - 10 entries with valid id (if you run the simulation in 10 minutes)
        - 10 entries with invalid id

    To generate an id we used the function token_urlsafe from secret library
    that returns a random URL-safe text string, containing 32 random bytes.

    To generate a device code we used the function token_urlsafe from secret library
    that returns a random URL-safe text string, containing 8 random bytes.

    """
    mydict = {}

    with open(filename, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile)   
        csvwriter.writerow(fields)
        
        for c in range (0,10):
            id_temp = secrets.token_urlsafe(32)
            device_code = "Android_"+secrets.token_urlsafe(8)
            id_time = datetime.datetime.now()   # time at this moment
            time_code = datetime.datetime.now()
            mydict = [ [id_temp, device_code, id_time, time_code] ]
            csvwriter.writerows(mydict)

        for c in range (0,10):
            id_temp = secrets.token_urlsafe(32)
            device_code = "Apple_"+secrets.token_urlsafe(8)
            id_time = datetime.datetime.now() - datetime.timedelta(minutes=15)  # time 15 minutes ago
            time_code = datetime.datetime.now() - datetime.timedelta(hours=6)   # time 6 hours ago
            mydict = [ [id_temp, device_code, id_time, time_code] ]
            csvwriter.writerows(mydict)
    
    shuffle_database()