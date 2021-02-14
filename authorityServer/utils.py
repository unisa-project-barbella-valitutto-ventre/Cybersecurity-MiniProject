import secrets
import datetime
import csv
import fileinput

def remove_code_after_24h(expired_date):
        lines = list()
        with open('database.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                if row[3] != expired_date:
                    lines.append(row)
        
        with open('database2.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)

def check_datetime_code(date_to_check):
    print(type(date_to_check))
    date_time_obj = datetime.datetime.strptime(date_to_check, '%Y-%m-%d %H:%M:%S.%f')
    current_time = datetime.datetime.now()
    print(type(current_time))
    t = (current_time - date_time_obj).total_seconds()
    print(t)

    if t > 86400:
        print("Codice scaduto")
        remove_code_after24h(date_time_obj)
        return False
    else:
        print("Codice valido")
        return True

def remove_ID_after_loaded(loaded, id_loaded):
    if loaded:
        with fileinput.input(files=('database.csv'), inplace=True, mode='r') as f:
            reader = csv.DictReader(f)
            print(",".join(reader.fieldnames))  # print back the headers
            for row in reader:
                if row['id'] == id_loaded:
                    row["id"] = "XXXXXX"
                print(",".join([row["id"],row["cod_device"], row["id_time"], row["cod_time"]]))

def remove_ID_after_10m(ID_date):
    with fileinput.input(files=('database.csv'), inplace=True, mode='r') as f:
        reader = csv.DictReader(f)
        print(",".join(reader.fieldnames))  # print back the headers
        for row in reader:
            if row['id_time'] == ID_date:
                row["id"] = "XXXXXX"
            print(",".join([row["id"],row["cod_device"], row["id_time"], row["cod_time"]]))

def check_id_date(ID_date):
    time1 = datetime.datetime.now()
    elapsed_time = (time1 - ID_date).total_seconds()
    print('Elapsed seconds: ', int(elapsed_time))

    if elapsed_time > 600:
        print("ID scaduto")
        remove_ID_after_10m(ID_date)
        return False
    else:
        print("Codice valido")
        return True

def check_id(ID_to_verify):
    i=0

    with open('database.csv', 'r') as readFile:
        reader = csv.DictReader(readFile, delimiter=',')
        for lines in reader:
            temp_id = lines['id']
            temp_id_date = lines['id_time']
            date_time_obj = datetime.datetime.strptime(temp_id_date, '%Y-%m-%d %H:%M:%S.%f')
            if temp_id == ID_to_verify:
                if check_id_date(date_time_obj):
                    i=1
                else:
                    i=2
            else:
                i=2
            
    if i==1:
        return True
    else:
        return False

def get_entry(cod_device):
    id_temp = secrets.token_urlsafe(32)
    id_time = datetime.datetime.now()
    time_code = datetime.datetime.now()
    return id_temp, id_time, time_code

if __name__ == "__main__":
    # mydict = {}
    # fields = ['id', 'cod_device', 'id_time', 'cod_time']
    # filename = "database.csv"
    # with open(filename, 'w') as csvfile:  
    #     csvwriter = csv.writer(csvfile)   
    #     csvwriter.writerow(fields)
    #     for c in range (0,10):
    #         id_temp, id_t, cod_t = get_entry(c)
    #         mydict = [ [id_temp, c, id_t, cod_t] ]
    #         csvwriter.writerows(mydict)  

    # remove_ID_after_10m('2021-02-13 10:52:01.228181')

    # remove_code_after_24h('2021-02-13 17:02:04.979664')
    # check_datetime_code('2021-02-13 17:02:04.978955')

    remove_ID_after_loaded(True, 'baOWopWMhV_z4Ew_fhWjeAQTfbC1-AYr5KxrEBcOE9c')

    # if check_id('K9BiqPFuTRbEl0DJRcEm9YZblJA1rLMoi4ZeKRKwoLc'):
    #     print('esiste')