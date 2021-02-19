import secrets
import datetime
import csv
import fileinput

STANDARD_ID = 'X'*43

'''
def remove_code_after_24h(expired_date):
    lines = list()
    with open('database.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            date_time_obj = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f')
            if (date_time_obj != expired_date):
                lines.append(row)

    fields = ['id', 'cod_device', 'id_time', 'cod_time']
    with open('database.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(fields)
        writer.writerows(lines)

def check_datetime_code(date_to_check):
    date_time_obj = datetime.datetime.strptime(date_to_check, '%Y-%m-%d %H:%M:%S.%f')
    current_time = datetime.datetime.now()
    t = (current_time - date_time_obj).total_seconds()
    print(t)

    if t > 86400:
        print("Device code not valid!")
        remove_code_after_24h(date_time_obj)
        return False
    else:
        print("Device code valid!")
        return True

# use this function to substitute id every 10 minutes in case of use of a thread
def remove_ID_after_10m(ID_date):
    with fileinput.input(files=('database.csv'), inplace=True, mode='r') as f:
        reader = csv.DictReader(f)
        print(",".join(reader.fieldnames)) 
        for row in reader:
            if row['id_time'] == ID_date:
                row["id"] = STANDARD_ID
            print(",".join([row["id"],row["cod_device"], row["id_time"], row["cod_time"]]))
'''

def replace_ID_after_loaded(id_loaded):
    """
    This function replace an Id field of a row with a default Id (STANDARD_ID).

    Args:
        id_loaded (string): Id to replace
    """
    with fileinput.input(files=('database.csv'), inplace=True, mode='r') as f:
        reader = csv.DictReader(f)
        print(",".join(reader.fieldnames))  # print back the headers
        for row in reader:
            if row['id'] == id_loaded:
                row["id"] = STANDARD_ID
            print(",".join([row["id"],row["cod_device"], row["id_time"], row["cod_time"]]))
                
def remove_id_row_after_10m(ID_date):
    """
    This function deletes an entire row using an ID_date associated to an Id.
    
    Args:
        ID_date (string): datetime to identify a row
    """
    lines = list()
    with open('database.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            date_time_obj = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
            if (date_time_obj != ID_date):
                lines.append(row)

    fields = ['id', 'cod_device', 'id_time', 'cod_time']
    with open('database.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(fields)
        writer.writerows(lines)

def check_id_date(ID_date):
    """
    This function checks the validity of an Id date
        - If time is elapsed it calls the remove_id_row_after_10m() function
    
    Args:
        ID_date (datetime): Id datetime to compare with current datetime
        
    Returns:
        [bool]: True if time is not elapsed, False otherwise
    """
    time1 = datetime.datetime.now()
    elapsed_time = (time1 - ID_date).total_seconds()
    print('Elapsed seconds: ', int(elapsed_time))

    if elapsed_time > 600:
        # print("ID to be removed")
        remove_id_row_after_10m(ID_date)
        return False
    else:
        print("Id Valid")
        return True

def check_id(ID_to_verify):
    """
    This function checks the validity of an Id.
    It calls the function check_id_date():
        - If True it calls replace_ID_after_loaded() and substitute the Id with a default value

    Args:
        ID_to_verify (string): ID to check

    Returns:
        [bool]: True if Id is still valid, False otherwise
    """

    if ID_to_verify != STANDARD_ID:
        with open('database.csv', 'r') as readFile:
            reader = csv.DictReader(readFile, delimiter=',')
            for lines in reader:
                temp_id = lines['id']
                temp_id_date = lines['id_time']
                # converting a string in a datetime object
                date_time_obj = datetime.datetime.strptime(temp_id_date, '%Y-%m-%d %H:%M:%S.%f')
                if temp_id == ID_to_verify:
                    if check_id_date(date_time_obj):
                        replace_ID_after_loaded(ID_to_verify)
                        return True

    return False

# if __name__ == "__main__":