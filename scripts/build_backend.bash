#!/bin/bash
# Builds server-side items, including apache config, secrets, and database

# setup and copy apache.conf
sed "s@\${EDCTF_DIR}@${EDCTF_DIR}@g" ${EDCTF_CONFIG}/apache.conf \
  | sed "s@\${EDCTF_DJANGO}@${EDCTF_DJANGO}@g" \
  | sed "s@\${EDCTF_STATIC}@${EDCTF_STATIC}@g" \
  | sed "s@\${EDCTF_FAVICON}@${EDCTF_FAVICON}@g" \
  | sed "s@\${EDCTF_ERROR_LOG}@${EDCTF_ERROR_LOG}@g" \
  | sed "s@\${EDCTF_ACCESS_LOG}@${EDCTF_ACCESS_LOG}@g" \
  | sudo bash -c "cat > ${APACHE_CONFIG}/000-default.conf"

# generate secrets and populate database
python ${EDCTF_SCRIPTS}/generate_secrets.py --output ${EDCTF_DJANGO}/edctf_secret.py \
  && cd ${EDCTF_DIR} \
  && python manage.py makemigrations \
  && python manage.py migrate \
  && python manage.py createsuperuser
