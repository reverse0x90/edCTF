#!/bin/bash
# Installs various dependancies using aptitude and pip.

sudo apt-get update \
  && sudo apt-get -y install \
    apache2 \
    libapache2-mod-wsgi \
    libpq-dev \
    postgresql \
    python-pip \
    python-dev \
    openssl \
  && sudo pip install -r ${EDCTF_SCRIPTS}/requirements.txt
