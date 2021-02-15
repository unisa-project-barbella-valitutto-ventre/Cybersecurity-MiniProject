import secrets
import datetime
import csv

# function to populate database

if __name__ == "__main__":
    mydict = {}

    fields = ['id', 'cod_device', 'id_time', 'cod_time']
    filename = "database.csv"
    with open(filename, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile)   
        csvwriter.writerow(fields)
        
        for c in range (0,10):
            id_temp = secrets.token_urlsafe(32)
            device_code = "Android_"+secrets.token_urlsafe(8)
            id_time = datetime.datetime.now()
            time_code = datetime.datetime.now()
            mydict = [ [id_temp, device_code, id_time, time_code] ]
            csvwriter.writerows(mydict)

        for c in range (0,10):
            id_temp = secrets.token_urlsafe(32)
            device_code = "Apple_"+secrets.token_urlsafe(8)
            id_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
            time_code = datetime.datetime.now() - datetime.timedelta(hours=6)
            mydict = [ [id_temp, device_code, id_time, time_code] ]
            csvwriter.writerows(mydict)