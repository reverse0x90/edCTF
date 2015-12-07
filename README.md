# edCTF

edCTF is a generic web application to quickly host jeopardy-style CTF competitions.  edCTF uses EmberJS for the client side of the application, while the backend utilizes the Django framework.

## Prerequisites

You will need the following things properly installed on your computer.

* [Docker](http://docs.docker.com/engine/installation/)

## Installation
Default installations set the Django superuser to username 'admin' with password 'admin'.  It is strongly recommended to change this password.

### Docker
You can run edCTF within a container with Docker via the following commands:
```
docker build -t edctf . \
  && docker run --restart=always -p 80:80 --name edctf_server -d edctf
```
edCTF can then be accessed on port 80 of your host machine.

### Local
You can also install edCTF locally, assuming you're using something similar to Ubuntu or Debian.

Simply run the production setup script:
```
./scripts/production.bash
```
edCTF will then be running on port 80 on your host machine.
