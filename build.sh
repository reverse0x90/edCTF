#!/bin/sh

export EDCTF_DIR=/opt/edctf
export EDCTF_STATIC_DIR=${EDCTF_DIR}/edctf/static
export DJANGO_STATIC_DIR=/usr/local/lib/python2.7/dist-packages/django/contrib/admin/static
export REST_FRAMEWORK_CSS_DIR=
export APACHE_CONFIG=/etc/apache2/sites-enabled/000-default.conf

sudo cp ${EDCTF_DIR}/apache.conf ${APACHE_CONFIG}

cd ${EDCTF_DIR}/ember \
  && npm install \
  && bower install \
  && ember build -prod -o ${EDCTF_STATIC_DIR}/ember \
  && mv ${EDCTF_STATIC_DIR}/ember/index.html ${EDCTF_DIR}/edctf/api/templates/index.html \
  && cp -R ${DJANGO_STATIC_DIR}/admin ${EDCTF_STATIC_DIR}/admin \
  && cp -R /usr/local/lib/python2.7/dist-packages/rest_framework/static/rest_framework ${EDCTF_STATIC_DIR}/rest_framework

cd ${EDCTF_DIR} \
  && python manage.py syncdb \
  && sudo chown $USER:www-data ${EDCTF_DIR} \
  && sudo chmod +w ${EDCTF_DIR} \
  && sudo chown $USER:www-data ${EDCTF_DIR}/*.sqlite3 \
  && sudo chmod +w ${EDCTF_DIR}/*.sqlite3
