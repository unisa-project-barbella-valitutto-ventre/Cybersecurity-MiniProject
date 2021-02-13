import secrets
import datetime
import csv
import fileinput

def remove_code_after24h(expired_date):
        lines = list()
        with open('database.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == expired_date:
                        print('if')
                        lines.remove(row)
                    else:
                        break

        with open('database.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            print('ho scritto')

def check_code(date_to_check):
    t = (datetime.datetime.now() - date_to_check).total_seconds()
    print(t)

    if t > 86400:
        print("Codice scaduto")
        remove_code_after24h(date_to_check)
        return False
    else:
        print("Codice valido")
        return True

def remove_ID_after10m(ID_date):

    with fileinput.input(files=('database.csv'), inplace=True, mode='r') as f:
        reader = csv.DictReader(f)
        print(",".join(reader.fieldnames))  # print back the headers
        for row in reader:
            if row['id_time'] == ID_date:
                row["id"] = "XXXXXX"
            print(",".join([row["id"],row["cod_device"], row["id_time"], row["cod_time"]]))


def check_id(ID_date):
    t = (datetime.datetime.now() - ID_date).total_seconds()
    print(t)

    if t > 600:
        print("ID scaduto")
        remove_ID_after10m(ID_date)
        return False
    else:
        print("Codice valido")
        return True

def get_entry(cod_device):
    id_temp = secrets.token_urlsafe(32)
    time_code = datetime.datetime.now()
    return id_temp, time_code, time_code

if __name__ == "__main__":
    # mydict = {}
    # fields = ['id', 'cod_device', 'id_time', 'cod_time']
    # filename = "database.csv"
    # with open(filename, 'w') as csvfile:  
    #     csvwriter = csv.writer(csvfile)   
    #     csvwriter.writerow(fields)
    #     for c in range (0,5):
    #         id_temp, id_t, cod_t = get_entry(c)
    #         mydict = [ [id_temp, c, id_t, cod_t] ]
    #         csvwriter.writerows(mydict)  

    # myTable = PrettyTable(["id", "cod", "id_time", "code_time"]) 
    # for c in range (0,5):
        
    #     id, id_t, cod_t = get_entry(c)
    #     # Add rows 
    #     myTable.add_row([id, c, id_t, cod_t])
    # print(myTable)

    # data = myTable.get_string()
    # with open('database.csv', 'wb') as f:
    #     f.write(data.encode())

    remove_ID_after10m('2021-02-13 10:52:01.228181')