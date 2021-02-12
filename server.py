#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65500        # Port to listen on (non-privileged ports are > 1023)

def process():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                if b'1' == data:
                    print("ID Accepted ! ACK sent.\n")
                    conn.sendall(b'ACK')
                else:                      
                    print("ID not found ! NACK sent.")
                    conn.sendall(b'NACK')

# -------- MAIN --------
if __name__ == '__main__':
    while True:
        process()