#!/usr/bin/env python3

import socket
import tkinter as tk
from tkinter import messagebox
import time


HOST = '127.0.0.1'
PORT = 65433

print("Example of Simulation\n")
time.sleep(1)
print("Checking Expositions...\n")
time.sleep(3)
print("Checking Expositions... DONE\n")
root = tk.Tk()
root.withdraw()
messagebox.showwarning('Notification Monitoring', 'Potential Exposure detected!\n')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'1') #Send ID
    data = s.recv(1024)

print('Received:', data.decode())

if data.decode() == 'ACK':
    print("\nDati caricati. Set F sul dispositivo\n")
    

if data.decode() == 'NACK':
    print("\nDati non caricati. Set T sul dispositivo\n")
