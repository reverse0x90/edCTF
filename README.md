# edCTF

edCTF is a generic web application to host jeopardy-style CTF competitions.  It uses both the EmberJS and Django frameworks.

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](http://git-scm.com/)
* [Docker](http://docs.docker.com/engine/installation/)

## Installation

You can run it within a container using Docker via the following commands:
```
docker build -t edctf .
docker run --restart=always -p 80:80 --name edctf_server -d edctf
```

Or you can install locally, assuming you're using something like Ubuntu or Debian.  Run this command in your shell:
```
sudo mkdir /opt/edctf \
&& sudo chown $USER:www-data /opt/edctf \
&& git clone https://github.com/IAryan/edCTF.git /opt/edctf \
&& sh /opt/edctf/all.sh
```
