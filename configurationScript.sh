#! /bin/bash

echo "Initial Configuration..."

# remove previous .pem and .txt files and specified directories

rm -rf *.pem
rm -rf rootCA
rm -rf intermediateCA
rm -f analiticsServer/counter.txt


echo "Building the rootCA directory"
# Build directory tree for rootCA (certs,private) and set up the initial files
mkdir rootCA
mkdir rootCA/private
mkdir rootCA/certs
touch rootCA/index.txt
touch rootCA/index.txt.attr
echo 01 > rootCA/serial

echo "Building the intermediateCA directory"
# Build directory tree for intermediateCA (certs,private) and set up the initial files
mkdir intermediateCA
mkdir intermediateCA/private
mkdir intermediateCA/certs
mkdir intermediateCA/csr
touch intermediateCA/index.txt
echo 01 > intermediateCA/serial

echo "Counter initialization"
touch analiticsServer/counter.txt
echo 0 > analiticsServer/counter.txt


echo "Installing pycryptodome libraries and python3 interpreter"
sleep 3
sudo apt install python3-pip
pip3 install pycryptodome

echo "Creating the rootCA private key"
openssl genrsa  -out rootCA/private/rootCAkey.pem 4096

echo "Creating self-signed certificate for the rootCA"
openssl req -new -x509 -days 3650 -extensions v3_ca -key rootCA/private/rootCAkey.pem -out rootCA/certs/rootCAcert.pem -config config/configCA.cnf -batch 

# Converting the certificate into in appropriate format for export_key() function in pycryptodome library
openssl x509 -in rootCA/certs/rootCAcert.pem -out rootCA/certs/rootCAcert.pem -outform PEM

echo "Creating the intermediateCA private key"
openssl genrsa -out intermediateCA/private/intermediateCAkey.pem 4096

echo "Creating a request to the rootCA to sign the intermediateCA certificate"
openssl req -new -sha256 -key intermediateCA/private/intermediateCAkey.pem -out intermediateCA/csr/intermediateCA.csr.pem -config config/configAnaliticsServer.cnf -batch

echo "Signing the intermediateCA certificate"
openssl ca -extensions v3_intermediate_ca -days 365 -notext -batch -in intermediateCA/csr/intermediateCA.csr.pem -out intermediateCA/certs/intermediateCAcert.pem -config config/configCA.cnf

# Converting the certificate into in appropriate format for export_key() function in pycryptodome library
openssl x509 -in intermediateCA/certs/intermediateCAcert.pem -out intermediateCA/certs/intermediateCAcert.pem -outform PEM

echo "Creating the certificates chain"
cat intermediateCA/certs/intermediateCAcert.pem rootCA/certs/rootCAcert.pem > intermediateCA/certs/rootCAIntermediateCA-chain.cert.pem

echo "Verifing the certificates chain"
# Additional operation to check if the certificates chain is correct or not
openssl verify -CAfile rootCA/certs/rootCAcert.pem intermediateCA/certs/intermediateCAcert.pem

echo "Initial Configuration Finished !"
sleep 3
