#!/bin/sh

sudo apt-get -y install apache2 libapache2-mod-wsgi python-pip python-dev git postgresql libpq-dev \
  && sudo pip install Django djangorestframework markdown django-filter \
  && (wget -qO- https://deb.nodesource.com/setup_4.x | sudo bash) \
  && sudo apt-get install -y nodejs \
  && sudo npm install -g ember-cli \
  && sudo npm install -g bower
