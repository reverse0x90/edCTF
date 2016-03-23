#!/bin/bash
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. ${WORKDIR}/environment.bash

set -x

# install frontend dependancies
sudo apt-get update \
  && sudo apt-get -y install \
    curl \
    git \
    npm
sudo npm cache clean -f && sudo npm install -g n && sudo n stable \
  && sudo npm install -g ember-cli \
  && sudo npm install -g bower

# build frontend
${WORKDIR}/build_frontend-dev.bash

# start apache/postgres
/usr/sbin/apache2ctl -k restart
service postgresql start

# recreate database backend
${WORKDIR}/reset_db.bash

# run bash as entrypoint
bash
