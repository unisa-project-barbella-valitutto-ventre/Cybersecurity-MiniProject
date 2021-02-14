
#! /bin/python3

import sys

sys.path.append('../')


import socket
import ssl

from analytics_parameters import ANALYTICS_SERVER_CERT_PATH, ANALYTICS_SERVER_KEY_PATH, AUTHORITY_SERVER_CERT_PATH
from analytics_parameters import COUNTRY_NAME_ISSUER, COMMON_NAME_ISSUER, ORGANIZATION_NAME_ISSUER


HOST = '127.0.0.1'
client_PORT = 8443
server_PORT = 8446

MAX_MESSAGE_SIZE = 43

def verify_server(cert):

    if not cert:
        raise Exception('')
    if ('commonName', COMMON_NAME_ISSUER) not in cert['issuer'][4] \
            or ('countryName', COUNTRY_NAME_ISSUER) not in cert['issuer'][0] \
            or ('organizationName', ORGANIZATION_NAME_ISSUER) not in cert['issuer'][3]:
        raise Exception("Certificate of Authority Server is not valid")


def send_data_to_server(data):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, server_PORT))
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(AUTHORITY_SERVER_CERT_PATH)
    context.load_cert_chain(certfile=ANALYTICS_SERVER_CERT_PATH, keyfile=ANALYTICS_SERVER_KEY_PATH)
    
    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock, server_side=False)


    cert = secure_sock.getpeercert()
    
    try:
        verify_server(cert)
    except Exception as e:
        print(str(e))
        raise SystemExit


    received_data = secure_sock.read(MAX_MESSAGE_SIZE)
    print(received_data.decode())

    secure_sock.write(data) #invio ID al Server

    received_data = secure_sock.read(MAX_MESSAGE_SIZE)

    ack_check = False
    if received_data.decode() == 'ACK':
        ack_check = True
        print("ACK received from Server.\n")


    if received_data.decode() == 'NACK':
        ack_check = False
        print("NACK received from Server.\n")

    secure_sock.close()
    sock.close()
    return ack_check

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, client_PORT))
    server_socket.listen(10)


    client, fromaddr = server_socket.accept()
    secure_sock = ssl.wrap_socket(client, server_side=True, certfile=ANALYTICS_SERVER_CERT_PATH, keyfile=ANALYTICS_SERVER_KEY_PATH)

    print(repr(secure_sock.getpeername()))
    print(secure_sock.cipher())
    print(secure_sock.getsockname())
    
    
    try:
        secure_sock.write(b"Analytics Server connected !")
        data = secure_sock.read(MAX_MESSAGE_SIZE)

        if len(data) != MAX_MESSAGE_SIZE:
            raise IndexError
        
        ack_check = send_data_to_server(data)
        if ack_check:
            count_read = open("counter.txt", "r").read()
            counter_update = int(count_read) + 1
            print(counter_update)
            count_write = open("counter.txt", "w")
            count_write.write(str(counter_update))    
            print("Counter Updated.\n")
            secure_sock.write(b'ACK') #invio dati al dispositivo

        else:
            print("Counter Not Updated.\n")
            secure_sock.write(b'NACK') #invio dati al dispositivo


    except IndexError as e:\
        secure_sock.write(b'NACK')
    
    finally:
        secure_sock.close()
        server_socket.close()



if __name__ == '__main__':
    print("*** ANALYTICS Server ***\n")
    while True:
        main()
