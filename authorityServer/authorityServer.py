#! /bin/python3

import sys
import code

sys.path.append('../')


import socket
import ssl


SERVER_CERT_PATH = "../rootCA/certs/rootCAcert.pem"
SERVER_KEY_PATH = "../rootCA/private/rootCAkey.pem"

HOST = '127.0.0.1'
PORT = 8446     # analityc server port

MESSAGE_SIZE = 1

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)


    client, fromaddr = server_socket.accept()
    secure_sock = ssl.wrap_socket(client, server_side=True, certfile=SERVER_CERT_PATH, keyfile=SERVER_KEY_PATH)

    print(repr(secure_sock.getpeername()))
    print(secure_sock.cipher())
    print(secure_sock.getsockname())
    
    
    try:
        secure_sock.write(b"Authority Server connected !")
        data = secure_sock.read(MESSAGE_SIZE)   # id dimension
        print("ID received: " + data.decode())
        
        if len(data) != MESSAGE_SIZE:
            raise IndexError

        # check id in database
        id_to_check = data.decode()
        if b'1' == data:
            secure_sock.write(b"ACK")
            print("ACK sent !\n")
        else:
            secure_sock.write(b"NACK")
            print("NACK sent !\n")

    except IndexError as e:\
        secure_sock.write(b'NACK')
    
    finally:
        secure_sock.close()
        server_socket.close()


if __name__ == '__main__':
    while True:
        main()
