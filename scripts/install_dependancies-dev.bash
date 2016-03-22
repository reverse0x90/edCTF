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
    npm \
    openssl \
    postgresql \
    python-pip \
    python-dev \
  && sudo pip install -r ${EDCTF_SCRIPTS}/requirements.txt \
  && (sudo npm cache clean -f && sudo npm install -g n && sudo n stable) \
  && sudo npm install -g ember-cli \
  && sudo npm install -g bower
