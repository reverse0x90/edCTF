#!/bin/bash
# Runs install, build, and run scripts to start within a develeopment environment

# set working directory
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set environment variables
source ${WORKDIR}/environment.bash

# attempt to destroy database
sudo -u postgres psql -c "DROP DATABASE ${EDCTF_DATABASE};"

# remove possible migration files
rm ${EDCTF_DJANGO}/api/migrations/*initial*

# run scripts
${WORKDIR}/install_dependancies.bash \
  && ${WORKDIR}/build_frontend.bash \
  && ${WORKDIR}/build_backend.bash \
  && ${WORKDIR}/start.bash
