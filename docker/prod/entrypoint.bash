#!/bin/bash
. ${SCRIPTS}/environment.bash
set -x

# Wait for postgres server to finish...
until netcat -z -w 2 db 5432; do sleep 1; done

# Build backend
${SCRIPTS}/build_backend.bash

# Entrypoint
/usr/sbin/apache2ctl -D FOREGROUND
