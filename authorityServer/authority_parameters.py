"""
This module contains parameters for client connection
"""
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

SERVER_CERT_PATH = "../rootCA/certs/rootCAcert.pem"
SERVER_KEY_PATH = "../rootCA/private/rootCAkey.pem"
CLIENT_CERT_PATH = "../intermediateCA/certs/rootCAIntermediateCA-chain.cert.pem"

COMMON_NAME = "www.AppServer.com"
ORGANIZATION_NAME = "Ministero della Salute"
COUNTRY_NAME = "IT"