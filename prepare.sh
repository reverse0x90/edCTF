#!/bin/sh

if [ -z "$EDCTF_DIR" ]; then
  export EDCTF_DIR=/opt/edCTF
fi
if [ -z "$EDCTF_STATIC_DIR" ]; then
  export EDCTF_STATIC_DIR=${EDCTF_DIR}/edctf/static
fi
if [ -z "$DJANGO_STATIC_DIR" ]; then
  export DJANGO_STATIC_DIR=/usr/local/lib/python2.7/dist-packages/django/contrib/admin/static
fi
if [ -z "$APACHE_CONFIG" ]; then
  export APACHE_CONFIG=/etc/apache2/sites-enabled/000-default.conf
fi


sudo (apt-get -y install apache2 libapache2-mod-wsgi python-pip git \
  && pip install Django djangorestframework markdown django-filter \
  && (wget -qO- https://deb.nodesource.com/setup_4.x | bash) \
  && apt-get install -y nodejs \
  && npm install -g ember-cli \
  && npm install -g bower)
