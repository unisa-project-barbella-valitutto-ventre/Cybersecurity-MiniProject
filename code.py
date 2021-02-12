import secrets
import datetime
from prettytable import PrettyTable , from_csv
import csv

def remove_code_after24h(code_date):
        lines = list()
        print('apro file csv')
        with open('database.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == code_date:
                        print('if')
                        lines.remove(row)
                    else:
                        break

        with open('database.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            print('ho scritto')

def check_code(dict_date):
    t = (datetime.datetime.now() - dict_date).total_seconds()
    print(t)

    if t > 86400:
        print("Codice scaduto")
        remove_code_after24h(dict_date)
        return False
    else:
        print("Codice valido")
        return False

def remove_ID_after10m(diz, ID_date):
    key = get_key(ID_date)
    try:
        del diz[key]
    except KeyError:
        print(f'Key {key} not found')

def check_id(diz, ID_date):
    t = (datetime.datetime.now() - ID_date).total_seconds()
    print(t)

    if t > 600:
        print("ID scaduto")
        remove_ID_after10m(diz, ID_date)
        return False
    else:
        print("Codice valido")
        return False

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
    remove_code_after24h('ZMnUC8g4eeE84ZCjXp4SoyrRocly9Liecc060DxeEGo')