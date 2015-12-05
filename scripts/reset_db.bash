#!/bin/bash
# Resets the edCTF database
# Used within the DEVELOPMENT environment.

# set working directory
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set environment variables
source ${WORKDIR}/environment.bash

# drop database
sudo -u postgres psql -c "DROP DATABASE ${EDCTF_DATABASE};"

# remove migration files
rm ${EDCTF_DJANGO}/api/migrations/*initial*

# regenerate database
${EDCTF_SCRIPTS}/build_backend.bash
