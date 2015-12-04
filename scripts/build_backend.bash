#!/bin/bash

sudo cp ${EDCTF_CONFIG}/apache.conf ${APACHE_CONFIG}/000-default.conf \
  && python ${EDCTF_SCRIPTS}/generate_secrets.py --output ${EDCTF_DJANGO}/edctf_secret.py \
  && cd ${EDCTF_DIR} \
  && python manage.py makemigrations \
  && python manage.py migrate \
  && python manage.py createsuperuser
