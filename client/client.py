#! /bin/python3

import socket
import ssl
import tkinter as tk
from tkinter import messagebox
import time

from client_parameters import COMMON_NAME, ANALYTICS_SERVER_CERT_PATH
from client_parameters import COUNTRY_NAME, ORGANIZATION_NAME, COUNTRY_NAME_ISSUER
from client_parameters import COMMON_NAME_ISSUER, ORGANIZATION_NAME_ISSUER
from id_read import read_csv

PATH_TO_CSV = "/../authorityServer/database.csv"

HOST = "127.0.0.1"
PORT = 8443
MAX_MESSAGE_SIZE = 43


def verify_server(cert):
    """
    This function verifies the correct certificate used by Analytics Server released by the Authority (Root CA)

    Args:
        cert : certificate to be verified

    Raises:
        Exception: if the certificate is not valid
    """
    
    if not cert:
        raise Exception('')
    if ('commonName', COMMON_NAME) not in cert['subject'][3] or ('countryName', COUNTRY_NAME) not in cert['subject'][
        0] or ('organizationName', ORGANIZATION_NAME) not in cert['subject'][2]:
        raise Exception("Certificate of Analytics Server is not valid")

    if ('commonName', COMMON_NAME_ISSUER) not in cert['issuer'][4] \
            or ('countryName', COUNTRY_NAME_ISSUER) not in cert['issuer'][0] \
            or ('organizationName', ORGANIZATION_NAME_ISSUER) not in cert['issuer'][3]:
        raise Exception("Certificate of Authority Server is not valid")


def send_data_to_server(data):
    """
    This function:
        - Opens a socket
        - Gets Analytics Server certificate and verifies it
        - Reads the welcome message from the Analytics Server
        - Sends the data to Analytics Server
        - Reads the response from the Analytics Server
        - Closes the socket

    Args:
        data (byte): id to send to Analytics Server

    Raises:
        SystemExit: if Analytics Server certificate is invalid
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(ANALYTICS_SERVER_CERT_PATH)
    secure_sock = context.wrap_socket(sock, server_hostname=HOST, server_side=False)

    cert = secure_sock.getpeercert()
    try:
        verify_server(cert)
    except Exception as e:
        print(str(e))
        raise SystemExit

    received_data = secure_sock.read(MAX_MESSAGE_SIZE)
    print(received_data.decode())
    
    secure_sock.write(data) #Send ID to Analytics Server

    received_data = secure_sock.read(MAX_MESSAGE_SIZE)
    print(received_data.decode())
    time.sleep(1)
    if received_data.decode() == 'ACK':
        print("Data loaded.\n")

    if received_data.decode() == 'NACK':
        print("Data not loaded.\n")

    secure_sock.close()
    sock.close()

if __name__ == '__main__':
    """
    We simulate two cases:
        - Before we read a valid id from database
        - After we read an invalid id from database
    """

    print("### Notification Counter for Contact Tracing DP3T ###\n")

    #ID valid
    print("Simulation with valid ID:")
    time.sleep(1)
    print("Checking Expositions...")
    time.sleep(2)
    print("Checking Expositions... DONE\n")
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning('Notification Monitoring', 'Potential Exposure detected!\n')
    id = read_csv(PATH_TO_CSV, True)
    # STANDARD_ID = 'X'*43
    send_data_to_server(str.encode(id))

    #ID not valid
    print("Simulation with not valid ID:")
    time.sleep(1)
    print("Checking Expositions...")
    time.sleep(2)
    print("Checking Expositions... DONE\n")
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning('Notification Monitoring', 'Potential Exposure detected!\n')
    id = read_csv(PATH_TO_CSV, False)
    send_data_to_server(str.encode(id))
    
    print("END of Simulation.\nYou can close all terminal windows.")
    time.sleep(7)
    
