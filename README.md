# edCTF
edCTF is a generic web application to rapidly deploy jeopardy-style CTF competitions.  edCTF utilizes both the EmberJS and Django frameworks to host CTFs. 

edCTF supports the ability to host multiple CTFs on the same application instance. There is no need to rebuild the framework.

edCTF can be quickly deployed using [Docker](https://github.com/docker/docker).

Current version: 2.0.0-beta

## Dependancies
* [Docker](http://docs.docker.com/engine/installation/)

## Installation
Default credentials for the admin account:
```
username: admin
password: admin
```
It is *strongly* recommended to change this password.

### Docker
You can run edCTF within a Docker container with the following commands:
```
docker build -t edctf . \
  && docker run --restart=unless-stopped -p 80:80 -p 443:443 -d edctf
```
edCTF can then be accessed at <http://localhost> or <https://localhost>

### Local
You can also install edCTF locally, assuming you're using something similar to Ubuntu or Debian.  Dependancies that are not listed above are installed with aptitude.

To deploy edCTF, run the production setup script:
```
./scripts/production.bash
```
edCTF can then be accessed via http or https your host machine.

### HTTPS
Before installation, in order to enable HTTPS, edit the USE_SSL variable within [environment.bash](scripts/environment.bash#L39) to "true".  edCTF will then generate a self-signed certificate for temporary use.  This method will be changed in a future release.

## Admin Panel
The admin panel is shown on the left after login.

If more technical changes are required, the django admin interface can be accessed at ```/djangoadmin/```

## Development
Development for edCTF can be performed using Docker or locally with [development.bash](scripts/development.bash).

### Docker
Build the edctf image locally:
```
docker build -t edctf .
```

To start your development container, run the following in your cloned repo:
```
docker run -it --restart=unless-stopped -p 8080:80 -p 4443:443 --entrypoint=/opt/edctf/scripts/start-docker-dev.bash -v "$PWD":/opt/edctf edctf
```
The server can be accessed at <https://localhost:8080>.

