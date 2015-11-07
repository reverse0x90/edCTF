#!/bin/sh

docker build -t edctf .
docker run --restart=always -p 80:80 -d edctf
#docker run --restart=always -p 443:443 -d edctf
