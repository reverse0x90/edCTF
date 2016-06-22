#!/bin/bash

# Install dependancies
sudo apt-get update \
  && sudo apt-get -y install \
    apache2 \
    libapache2-mod-wsgi \
    libpq-dev \
    openssl \
    python-pip \
    python-dev
sudo pip install -r "${EDCTF_DIR}/requirements.txt"

# Build Django admin css
sudo cp -R "${DJANGO_ADMIN_STATIC}" "${EDCTF_ADMIN_STATIC}"

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
