FROM ubuntu:trusty

# Install dependancies and intialize
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install apache2 libapache2-mod-wsgi python-pip git \
  && pip install Django djangorestframework markdown django-filter \
  && mkdir /opt/edctf \
  && useradd -m edctf \
  && chown edctf:edctf /opt/edctf

# Add apache config
ADD apache.conf /etc/apache2/sites-enabled/000-default.conf

# Switch to edctf user
USER edctf

# add ember and django files
ADD ember /opt/edctf/ember
ADD edctf /opt/edctf/edctf
ADD manage.py /opt/edctf/manage.py

# Install Ember dependancies and move client-side files
RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.29.0/install.sh | bash
RUN nvm install v4.1.2 \
  && nvm alias default v4.1.2 \
  && npm install -g ember-cli \
  && npm install -g bower \
  && cd /opt/edctf/ember \
  && npm install \
  && bower install \
  && ember build -prod -o /opt/edctf/edctf/static/ember \
  && mv /opt/edctf/edctf/static/ember/index.html /opt/edctf/edctf/api/templates/index.html


USER root
EXPOSE 80 443
CMD /usr/sbin/apache2ctl -D FOREGROUND
