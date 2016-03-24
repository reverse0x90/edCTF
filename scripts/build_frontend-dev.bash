#!/bin/bash
# Generates client-side items, including building ember and copying CSS

set -x

cd ${EDCTF_EMBER} \
  && sudo npm install \
  && bower install -q \
  && ember build -prod -o ${EDCTF_EMBER_STATIC} \
  && cp -R ${DJANGO_ADMIN_STATIC} ${EDCTF_ADMIN_STATIC} \
  && cp -R ${REST_FRAMEWORK_CSS_DIR} ${EDCTF_REST_STATIC}
