#!/bin/bash
set -x

. ${SCRIPTS}/environment.bash

# Start services
/etc/init.d/postgresql start

# Build backend
${SCRIPTS}/build_backend.bash

# Entrypoint
/usr/sbin/apache2ctl -D FOREGROUND
