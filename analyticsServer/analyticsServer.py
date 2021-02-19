
#! /bin/python3

import sys
import socket
import ssl
import time
from analytics_parameters import *

sys.path.append('../')

HOST = '127.0.0.1'
client_PORT = 8443
server_PORT = 8446
MAX_MESSAGE_SIZE = 43

def verify_server(cert):
    """
    This function verifies the correct certificate used by Authority Server

    Args:
        cert : the certificate to verify

    Raises:
        Exception: if the certificate of Authority Server is not valid
    """
    if not cert:
        raise Exception('')
    if ('commonName', COMMON_NAME_ISSUER) not in cert['issuer'][4] \
            or ('countryName', COUNTRY_NAME_ISSUER) not in cert['issuer'][0] \
            or ('organizationName', ORGANIZATION_NAME_ISSUER) not in cert['issuer'][3]:
        raise Exception("Certificate of Authority Server is not valid")


def send_data_to_server(data):
    """
    This function:
        - Opens a socket
        - Gets Authority Server certificate and verifies it
        - Reads the welcome message from the Authority Server
        - Sends the data to Authority Server
        - Reads the response from the Authority Server
        - Closes the socket

    Args:
        data (byte): id received from device and sent to Authority Server

    Raises:
        SystemExit: 

    Returns:
        [bool]: ACK if it received ack from Authority Server, otherwise NACK
    """

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
    print("Sending ID to Server...")
    secure_sock.write(data) #Forward ID to authoritative Server
    print("Waiting for the response...")
    received_data = secure_sock.read(MAX_MESSAGE_SIZE)

    time.sleep(2)
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
    """
    This function:
        - Opens a socket
        - Reads id from device
        - Opens a connection to the Authority Server
        - Reads the response from the Authority Server
            If receives ack:
                Update the counter
        - Sends the response to the device
        - Closes the socket

    Raises:
        IndexError: sends NACK if the message size is wrong
    """
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
        
        time.sleep(1)
        ack_check = send_data_to_server(data)
        time.sleep(2)
        if ack_check:
            count_read = open("counter.txt", "r").read()
            counter_update = int(count_read) + 1
            #print(counter_update)
            count_write = open("counter.txt", "w")
            count_write.write(str(counter_update))    
            print("Counter Updated: " + str(counter_update))
            secure_sock.write(b'ACK') #Send ACK to device

        else:
            count_read = open("counter.txt", "r").read()
            print("Counter Not Updated: " + count_read)
            secure_sock.write(b'NACK') #Send NACK to device

    except IndexError as e:\
        secure_sock.write(b'NACK')
    
    finally:
        secure_sock.close()
        server_socket.close()

if __name__ == '__main__':
    print("*** ANALYTICS Server ***\n")
    
    # 3 is the number of ID received from the client
    for i in range (0,3):
        main()
        print("--------------\n")

    print("Simulation ended!")
    time.sleep(3)

