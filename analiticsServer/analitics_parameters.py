"""
This module contains parameters for client connection
"""
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


ANALITICS_SERVER_CERT_PATH = "../intermediateCA/certs/rootCAIntermediateCA-chain.cert.pem"
ANALITICS_SERVER_KEY_PATH = "../intermediateCA/private/intermediateCAkey.pem"

AUTHORITY_SERVER_CERT_PATH = "../rootCA/certs/rootCAcert.pem"

COUNTRY_NAME_ISSUER = "IT"
COMMON_NAME_ISSUER = "ministero.gov.salute"
ORGANIZATION_NAME_ISSUER = "Ministero della Salute"
