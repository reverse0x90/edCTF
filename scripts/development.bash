#!/bin/bash
# Runs install, build, and run scripts to start within a develeopment environment

export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. ${WORKDIR}/environment.bash

set -x

# attempt to destroy database
sudo -u postgres psql -c "DROP DATABASE ${EDCTF_DATABASE};"

# remove possible migration files
rm ${EDCTF_DJANGO}/api/migrations/*initial*

# run scripts
${WORKDIR}/install_dependancies-dev.bash \
  && ${WORKDIR}/build_frontend-dev.bash \
  && ${WORKDIR}/build_backend.bash \
  && ${WORKDIR}/start.bash
