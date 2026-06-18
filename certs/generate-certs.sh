#!/bin/bash

OUT_DIR="generated/"
mkdir -p ${OUT_DIR}

echo "Generating ca..."
openssl req -x509 -nodes -newkey rsa:2048 -keyout ${OUT_DIR}ca.key -out ${OUT_DIR}ca.crt  -subj "//CN=MonitoringCA"

echo -e "[v3_ext]\nsubjectAltName=DNS:tomcat" > ${OUT_DIR}san.cnf

echo "Generating monitor certs..."
openssl req -new -nodes -newkey rsa:2048 -keyout ${OUT_DIR}monitor.key -out ${OUT_DIR}monitor.csr -subj "//CN=monitor"  
openssl x509 -req -in ${OUT_DIR}monitor.csr -CA ${OUT_DIR}ca.crt -CAkey ${OUT_DIR}ca.key -out ${OUT_DIR}monitor.crt

echo "Generating server certs..."
openssl req -new -nodes -newkey rsa:2048 -keyout ${OUT_DIR}tomcat.key -out ${OUT_DIR}tomcat.csr -subj "//CN=tomcat"
openssl x509  -extfile san.cnf -extensions v3_ext -req -in ${OUT_DIR}tomcat.csr -CA ${OUT_DIR}ca.crt -CAkey ${OUT_DIR}ca.key -out ${OUT_DIR}tomcat.crt
