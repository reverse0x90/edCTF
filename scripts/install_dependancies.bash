#!/bin/bash
# Installs various dependancies using aptitude and pip.
# Installs npm, bower, and ember via node from nodesource.

sudo apt-get -y install apache2 libapache2-mod-wsgi python-pip python-dev git postgresql libpq-dev \
  && sudo pip install -r ${EDCTF_SCRIPTS}/requirements.txt \
  && (wget -qO- https://deb.nodesource.com/setup_4.x | sudo bash) \
  && sudo apt-get install -y nodejs \
  && sudo npm install -g ember-cli \
  && sudo npm install -g bower
