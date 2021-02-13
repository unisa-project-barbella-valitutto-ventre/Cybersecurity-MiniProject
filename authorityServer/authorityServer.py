#! /bin/python3

import sys
import code

sys.path.append('../')


import socket
import ssl
#import pprint

from authority_parameters import SERVER_CERT_PATH, SERVER_KEY_PATH, CLIENT_CERT_PATH
from authority_parameters import COMMON_NAME, ORGANIZATION_NAME, COUNTRY_NAME

HOST = '127.0.0.1'
PORT = 8446     # analitycserver port

MESSAGE_SIZE = 1

def verify_client(cert):

    if not cert:
        raise Exception('')
    if ('commonName', COMMON_NAME) not in cert['subject'][3] or ('countryName', COUNTRY_NAME) not in cert['subject'][
        0] or ('organizationName', ORGANIZATION_NAME) not in cert['subject'][2]:
        raise Exception("Certificate of Analitics Server is not valid")



def main():


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)


    client, fromaddr = server_socket.accept()
    secure_sock = ssl.wrap_socket(client, server_side=True, ca_certs=CLIENT_CERT_PATH, certfile=SERVER_CERT_PATH,
    keyfile=SERVER_KEY_PATH, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2)

    print(repr(secure_sock.getpeername()))
    print(secure_sock.cipher())
    #print(pprint.pformat(secure_sock.getpeercert()))
    
    cert = secure_sock.getpeercert()

    try:
        verify_client(cert)
    except Exception as e:
        print(str(e))
        raise SystemExit
    
    
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
    print("*** AUTHORITY Server ***\n")
    while True:
        main()

