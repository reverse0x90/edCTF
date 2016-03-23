#!/bin/bash

. ${SCRIPTS}/environment.bash

set -x

#npm install -g ember-cli
#npm install -g bower

# Build frontend
#${SCRIPTS}/build_frontend-dev.bash

# start services
/usr/sbin/apache2ctl -k restart \
  && /etc/init.d/postgresql start

# Entrypoint
/bin/bash
