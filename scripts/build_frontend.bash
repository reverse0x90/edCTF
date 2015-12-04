#!/bin/bash

cd ${EDCTF_EMBER} \
  && npm install \
  && bower install \
  && ember build -prod -o ${EDCTF_EMBER_STATIC} \
  && cp -R ${DJANGO_ADMIN_STATIC} ${EDCTF_ADMIN_STATIC} \
  && cp -R ${REST_FRAMEWORK_CSS_DIR} ${EDCTF_REST_STATIC}
