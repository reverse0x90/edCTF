#!/bin/bash
# Builds server-side items, including apache config, secrets, and database

SCRIPTS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. "${SCRIPTS}/environment.bash"

# if USE_SSL set to true generate self-signed cert and enable ssl
if [ "$USE_SSL" = "true" ]
then
  # create location to save the self-signed cert
  if [ ! -d "$SSL_DIR" ]
  then
    sudo bash -c "mkdir ${SSL_DIR}"
  fi

  # generate self-signed ssl cert
  sudo bash -c "openssl genrsa -des3 -passout pass:x -out ${SSL_DIR}/server.pass.key 2048" \
   && sudo bash -c "openssl rsa -passin pass:x -in ${SSL_DIR}/server.pass.key -out ${SSL_DIR}/server.key" \
   && sudo bash -c "openssl req -new -key ${SSL_DIR}/server.key -out ${SSL_DIR}/server.csr -subj \"/C=${SSL_COUNTRY}/ST=${SSL_STATE}/L=${SSL_LOCALITY}/O=${SSL_ORGANIZATION}/OU=${SSL_OU}/CN=${SSL_CN}\"" \
   && sudo bash -c "openssl x509 -req -days 365 -in ${SSL_DIR}/server.csr -signkey ${SSL_DIR}/server.key -out ${SSL_DIR}/server.crt" \
   && sudo bash -c "rm ${SSL_DIR}/server.pass.key" \
   && sudo bash -c "chmod 600 ${SSL_DIR}"

  # enable apache mod rewrite
  sudo a2enmod rewrite

  # enable apache mod ssl
  sudo a2enmod ssl

  # setup and copy apache-ssl.conf
  sed "s@\${EDCTF_DIR}@${EDCTF_DIR}@g" ${EDCTF_CONFIG_HTTPS}/apache-ssl.conf \
    | sed "s@\${EDCTF_DJANGO}@${EDCTF_DJANGO}@g" \
    | sed "s@\${EDCTF_STATIC}@${EDCTF_STATIC}@g" \
    | sed "s@\${EDCTF_FAVICON}@${EDCTF_FAVICON}@g" \
    | sed "s@\${EDCTF_ERROR_LOG}@${EDCTF_ERROR_LOG}@g" \
    | sed "s@\${EDCTF_ACCESS_LOG}@${EDCTF_ACCESS_LOG}@g" \
    | sudo bash -c "cat > ${APACHE_CONFIG}/default-ssl.conf"

  # Copy the modrewrite date
  sudo bash -c "cat ${EDCTF_CONFIG_HTTPS}/apache.conf > ${APACHE_CONFIG}/000-default.conf"
else
  # setup and copy apache.conf
  sed "s@\${EDCTF_DIR}@${EDCTF_DIR}@g" ${EDCTF_CONFIG_HTTP}/apache.conf \
    | sed "s@\${EDCTF_DJANGO}@${EDCTF_DJANGO}@g" \
    | sed "s@\${EDCTF_STATIC}@${EDCTF_STATIC}@g" \
    | sed "s@\${EDCTF_FAVICON}@${EDCTF_FAVICON}@g" \
    | sed "s@\${EDCTF_ERROR_LOG}@${EDCTF_ERROR_LOG}@g" \
    | sed "s@\${EDCTF_ACCESS_LOG}@${EDCTF_ACCESS_LOG}@g" \
    | sudo bash -c "cat > ${APACHE_CONFIG}/000-default.conf"
fi
set -x
# generate secrets and populate database
python "${EDCTF_SCRIPTS}/generate_secrets.py" --dbhost "${DB_HOST}" --dbpass "${DB_PASS}" --output "${EDCTF_DJANGO}/edctf_secret.py" \
  && python "${EDCTF_DIR}/manage.py" makemigrations \
  && python "${EDCTF_DIR}/manage.py" migrate auth \
  && python "${EDCTF_DIR}/manage.py" migrate \
  && echo "from django.contrib.auth import get_user_model
from edctf.api.models import Team
user = get_user_model().objects.create_superuser('admin', 'admin@localhost', 'admin')
team = Team.objects.create_team('admin', user)" \
  | python "${EDCTF_DIR}/manage.py" shell
