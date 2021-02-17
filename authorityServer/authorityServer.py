#! /bin/python3

import sys
import socket
import ssl
import time
from utils import check_id
from authority_parameters import *

sys.path.append('../')

HOST = '127.0.0.1'
PORT = 8446     # analitycserver port
MESSAGE_SIZE = 43 # dimension of 32 byte encoded in Base64

def verify_client(cert):
    """
    This function verifies the correct certificate used by Analytics Server released by the authority

    Args:
        cert : certificate to verify

    Raises:
        Exception: if certificate is not valid
    """
    if not cert:
        raise Exception('')
    if ('commonName', COMMON_NAME) not in cert['subject'][3] or ('countryName', COUNTRY_NAME) not in cert['subject'][
        0] or ('organizationName', ORGANIZATION_NAME) not in cert['subject'][2]:
        raise Exception("Certificate of Analytics Server is not valid")

def main():
    """
     This function:
        - Opens a socket
        - Gets the Analytics Server certificate and verifying it
        - Sends the welcome message to the Analytics Server
        - Reads the response from the Analytics Server
        - Closes the socket

    Raises:
        SystemExit: 
        IndexError: send a NACK to Analytics Server
    """
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
        data = secure_sock.read(MESSAGE_SIZE)   # id received from analytics server
        print("ID from analytics server: " + data.decode())
        
        if len(data) != MESSAGE_SIZE:
            raise IndexError

        # check id in database
        id_to_check = data.decode()
        if check_id(id_to_check):
            time.sleep(1)
            secure_sock.write(b"ACK")
            print("ACK sent !\n")
        else:
            time.sleep(1)
            secure_sock.write(b"NACK")
            print("NACK sent !\n")

    except IndexError as e:\
        secure_sock.write(b'NACK')
    
    finally:
        secure_sock.close()
        server_socket.close()



if __name__ == '__main__':
    print("*** AUTHORITY Server ***\n")
    
    # 3 is the number of ID received from Analytics Server
    for i in range (0,3):
        main()
    print("Simulation ended!")
    time.sleep(1)