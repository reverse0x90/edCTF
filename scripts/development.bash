#!/bin/bash

# Install dependancies
sudo apt-get update \
  && sudo apt-get -y install \
    apache2 \
    curl \
    libapache2-mod-wsgi \
    libpq-dev \
    git \
    npm \
    openssl \
    python-pip \
    python-dev
sudo pip install -r ${EDCTF_DIR}/requirements.txt

# Update npm
sudo npm install -g n \
  && sudo n 0.12.12

# Install ember and bower
sudo npm install -g ember-cli
sudo npm install -g bower

# Install ember dependancies
cd ${EDCTF_EMBER} \
  && npm install \
  && bower install -q

# Copy css
sudo cp -R ${DJANGO_ADMIN_STATIC} ${EDCTF_ADMIN_STATIC} \
  && sudo cp -R ${REST_FRAMEWORK_CSS_DIR} ${EDCTF_REST_STATIC}

# Setup database
(sudo -u postgres psql -c "CREATE USER edctf WITH PASSWORD '${DB_PASS}';") \
    || (sudo -u postgres psql -c "ALTER USER edctf WITH PASSWORD '${DB_PASS}';")
sudo -u postgres psql -c "DROP DATABASE edctf;"
sudo -u postgres psql -c "CREATE DATABASE edctf;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE edctf to edctf;"

# Build backend
${SCRIPTS}/build_backend.bash

# Restart apache
sudo /usr/sbin/apache2ctl -k restart
