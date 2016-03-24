#!/bin/bash

. ${SCRIPTS}/environment.bash

set -x

# Build frontend
${SCRIPTS}/build_frontend-dev.bash

# start services
/usr/sbin/apache2ctl -k restart \
  && /etc/init.d/postgresql start

# Entrypoint
/bin/bash
