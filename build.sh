#!/bin/sh

sudo cp apache.conf ${APACHE_CONFIG}

cd ${EDCTF_DIR}/ember \
  && npm install \
  && bower install \
  && ember build -prod -o ${EDCTF_STATIC_DIR}/ember \
  && mv ${EDCTF_STATIC_DIR}/ember/index.html ${EDCTF_DIR}/edctf/api/templates/index.html \
  && cp -R ${DJANGO_STATIC_DIR}/admin ${EDCTF_STATIC_DIR}/admin \
  && cp -R /usr/local/lib/python2.7/dist-packages/rest_framework/static/rest_framework ${EDCTF_STATIC_DIR}/rest_framework

python manage.py syncdb

sudo chown $USER:www-data *.sqlite3
