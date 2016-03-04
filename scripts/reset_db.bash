#!/bin/bash
# Resets the edCTF database
# Used within the DEVELOPMENT environment.

sudo apachectl stop

# set working directory
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set environment variables
source ${WORKDIR}/environment.bash

# drop database
sudo -u postgres psql -c "DROP DATABASE ${EDCTF_DATABASE};"

# remove migration files
find ${EDCTF_DJANGO}/api/migrations/ -type f -not -name '__init__.py' -and -not -name '.gitignore' -exec rm {} +

# regenerate database
${EDCTF_SCRIPTS}/build_backend.bash

# restart service
${EDCTF_SCRIPTS}/start.bash
