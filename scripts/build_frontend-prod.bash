#!/bin/bash
# Generates client-side items, including building ember and copying CSS

cp -R ${DJANGO_ADMIN_STATIC} ${EDCTF_ADMIN_STATIC} \
  && cp -R ${REST_FRAMEWORK_CSS_DIR} ${EDCTF_REST_STATIC}
