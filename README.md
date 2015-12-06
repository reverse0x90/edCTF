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
The default Django admin credentials are admin/admin.  Also, it is not recommended to run docker commands as a root/sudo user.


You can also install locally, assuming you're using something like Ubuntu.  Run the production setup script:
```
scripts/production.bash
```
