#!/bin/bash
# Resets the edCTF database
# Used within the DEVELOPMENT environment.

WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. "${WORKDIR}/environment.bash"

set -x

# stop apache
sudo apachectl stop

# drop database
sudo -u postgres psql -c "DROP DATABASE ${EDCTF_DATABASE};"

# remove migration files
find "${EDCTF_DJANGO}/api/migrations/" -type f -not -name '__init__.py' -and -not -name '.gitignore' -exec rm {} +

# regenerate database
"${EDCTF_SCRIPTS}/build_backend.bash"

# restart apache
sudo apachectl start
