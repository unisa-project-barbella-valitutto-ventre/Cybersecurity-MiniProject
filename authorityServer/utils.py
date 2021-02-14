import secrets
import datetime
import csv
import fileinput

standard_id = 'X'*43

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

def remove_ID_after_loaded(loaded, id_loaded):
    if loaded:
        with fileinput.input(files=('database.csv'), inplace=True, mode='r') as f:
            reader = csv.DictReader(f)
            print(",".join(reader.fieldnames))  # print back the headers
            for row in reader:
                if row['id'] == id_loaded:
                    row["id"] = standard_id
                print(",".join([row["id"],row["cod_device"], row["id_time"], row["cod_time"]]))

# use this function to substitute id every 10 minutes in case of use of a thread
def remove_ID_after_10m(ID_date):
    with fileinput.input(files=('database.csv'), inplace=True, mode='r') as f:
        reader = csv.DictReader(f)
        print(",".join(reader.fieldnames)) 
        for row in reader:
            if row['id_time'] == ID_date:
                row["id"] = standard_id
            print(",".join([row["id"],row["cod_device"], row["id_time"], row["cod_time"]]))
'''

# Delete entire row using an ID_date relative to ID_loaded
def remove_all_after_10m(ID_date):
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

# function to check validity of ID date
def check_id_date(ID_date):
    time1 = datetime.datetime.now()
    elapsed_time = (time1 - ID_date).total_seconds()
    print('Elapsed seconds: ', int(elapsed_time))

    if elapsed_time > 600:
        print("ID to be removed")
        remove_all_after_10m(ID_date)
        return False
    else:
        print("Id valid")
        return True

# function to check validity of an ID
def check_id(ID_to_verify):
    i=0
    if ID_to_verify != standard_id:
        with open('database.csv', 'r') as readFile:
            reader = csv.DictReader(readFile, delimiter=',')
            for lines in reader:
                temp_id = lines['id']
                temp_id_date = lines['id_time']
                date_time_obj = datetime.datetime.strptime(temp_id_date, '%Y-%m-%d %H:%M:%S.%f')
                if temp_id == ID_to_verify:
                    print('id sono uguali')
                    if check_id_date(date_time_obj):
                        print('flag')
                        i=1
                        break
                    else:
                        i=2
                else:
                    i=3
    else:
        i=4

    if i==1:
        return True
    else:
        return False

# function to populate database
def get_entry(cod_device):
    id_temp = secrets.token_urlsafe(32)
    id_time = datetime.datetime.now()
    time_code = datetime.datetime.now()
    return id_temp, id_time, time_code

# if __name__ == "__main__":
#     mydict = {}
#     fields = ['id', 'cod_device', 'id_time', 'cod_time']
#     filename = "database.csv"
#     with open(filename, 'w') as csvfile:  
#         csvwriter = csv.writer(csvfile)   
#         csvwriter.writerow(fields)
#         for c in range (0,10):
#             id_temp, id_t, cod_t = get_entry(c)
#             mydict = [ [id_temp, c, id_t, cod_t] ]
#             csvwriter.writerows(mydict)  