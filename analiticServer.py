#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  
client_PORT = 65433
server_PORT = 65500

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, client_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data_client = conn.recv(1024) #Received ID
            if not data_client:
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, server_PORT))
                s.sendall(data_client) #Send ID to Server
                data_server = s.recv(1024)
            print('Received:', data_server.decode())

            if data_server.decode() == 'ACK':
                #incrementare counter
                count_read = open("counter.txt", "r").read()
                counter_update = int(count_read) + 1
                print(counter_update)
                count_write = open("counter.txt", "w")
                count_write.write(str(counter_update))
                print("\nCounter Aggiornato.\n")
                conn.sendall(b'ACK') #invio dati al dispositivo          

            if data_server.decode() == 'NACK':
                print("\nCounter Non Aggiornato\n")
                conn.sendall(b'NACK') #invio dati al dispositivo