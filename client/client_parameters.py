"""
This module contains parameters for client connection
"""
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


COMMON_NAME = "www.AppServer.com"
ANALITICS_SERVER_CERT_PATH = "../intermediateCA/certs/rootCAIntermediateCA-chain.cert.pem"

COUNTRY_NAME = "IT"
ORGANIZATION_NAME = "Ministero della Salute"

COUNTRY_NAME_ISSUER = "IT"
COMMON_NAME_ISSUER = "ministero.gov.salute"
ORGANIZATION_NAME_ISSUER = "Ministero della Salute"