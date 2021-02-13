#! /bin/python3

import socket
import ssl
import tkinter as tk
from tkinter import messagebox
import time

COMMON_NAME = "www.AppServer.com"
APP_SERVER_CERT_PATH = "../intermediateCA/certs/rootCAIntermediateCA-chain.cert.pem"
HOST = "127.0.0.1"
PORT = 8443
MAX_MESSAGE_SIZE = 512

COUNTRY_NAME = "IT"
ORGANIZATION_NAME = "Ministero della Salute"

COUNTRY_NAME_ISSUER = "IT"
COMMON_NAME_ISSUER = "ministero.gov.salute"
ORGANIZATION_NAME_ISSUER = "Ministero della Salute"


def verify_server(cert):
    """
    This function verifies the correct certificate used by App Server released by the authorities
    :param cert: the certificate to be verified
    :return: None
    :raise Exception: if the certificate is not valid
    """
    if not cert:
        raise Exception('')
    if ('commonName', COMMON_NAME) not in cert['subject'][3] or ('countryName', COUNTRY_NAME) not in cert['subject'][
        0] or ('organizationName', ORGANIZATION_NAME) not in cert['subject'][2]:
        raise Exception("Certificate of intermediateCA is not valid")

    if ('commonName', COMMON_NAME_ISSUER) not in cert['issuer'][4] \
            or ('countryName', COUNTRY_NAME_ISSUER) not in cert['issuer'][0] \
            or ('organizationName', ORGANIZATION_NAME_ISSUER) not in cert['issuer'][3]:
        raise Exception("Certificate of rootCA is not valid")


def send_data_to_server(data):
    """
    This function contains:
        - Opening a socket
        - Getting the server certificate and verifying it
        - Reading the welcome message from the server
        - Reading the report response from the server
        - Closing the socket
    :param data:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(APP_SERVER_CERT_PATH)
    secure_sock = context.wrap_socket(sock, server_hostname=HOST, server_side=False)

    cert = secure_sock.getpeercert()
    try:
        verify_server(cert)
    except Exception as e:
        print(str(e))
        raise SystemExit


    received_data = secure_sock.read(MAX_MESSAGE_SIZE)
    print(received_data.decode())

    secure_sock.write(data) #invio ID al Server di Analisi

    received_data = secure_sock.read(MAX_MESSAGE_SIZE)
    print(received_data.decode())

    if received_data.decode() == 'ACK':
        print("\nDati caricati. Set F sul dispositivo\n")
    #Da fare: return bool

    if received_data.decode() == 'NACK':
        print("\nDati non caricati. Set T sul dispositivo\n")
    #Da fare: return bool


    secure_sock.close()
    sock.close()
    
if __name__ == '__main__':
    #send ID to analitics server: ID = 1
    print("Example of Simulation\n")
    time.sleep(1)
    print("Checking Expositions...\n")
    time.sleep(3)
    print("Checking Expositions... DONE\n")
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning('Notification Monitoring', 'Potential Exposure detected!\n')
    
    send_data_to_server(b'1')

