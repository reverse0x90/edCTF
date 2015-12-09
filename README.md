# edCTF

edCTF is a generic web application to quickly host jeopardy-style CTF competitions.  edCTF uses EmberJS for the client half of the application, while the backend utilizes the Django framework.


Current version: 1.1-beta1

## Prerequisites

You will need the following things properly installed on your computer.

* [Docker](http://docs.docker.com/engine/installation/)

## Installation
The following installation methods will set the Django superuser username to 'admin' with 'admin' as the password.  It is *strongly* recommended to change this password.

### Docker
You can run edCTF within a Docker container with the following commands:
```
**SSL disabled:**
docker build -t edctf . \
  && docker run --restart=always -p 80:80 --name edctf_server -d edctf


**SSL enabled:**
docker build -t edctf . \
  && docker run --restart=always -p 80:80 -p 443:443 --name edctf_server -d edctf
```
edCTF can then be accessed on port 80 of your host machine.

### Local
You can also install edCTF locally, assuming you're using something similar to Ubuntu or Debian.

Simply run the production setup script:
```
./scripts/production.bash
```
edCTF will then be running on port 80 on your host machine.
