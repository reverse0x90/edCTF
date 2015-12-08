#!/bin/bash
# Installs various dependancies using aptitude and pip.
# Installs npm, bower, and ember via node from nodesource.

sudo apt-get update \
  && sudo apt-get -y install \
    apache2 \
    curl \
    git \
    libapache2-mod-wsgi \
    libpq-dev \
    postgresql \
    python-pip \
    python-dev \
  && sudo pip install -r ${EDCTF_SCRIPTS}/requirements.txt \
  && (curl -sL https://deb.nodesource.com/setup | sudo bash -) \
  && sudo apt-get install -y nodejs \
  && sudo npm install -g ember-cli \
  && sudo npm install -g bower
