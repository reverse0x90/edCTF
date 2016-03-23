#!/bin/bash
# Runs install, build, and run scripts to start within a production environment

export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. ${WORKDIR}/environment.bash

set -x

# run scripts
${WORKDIR}/install_dependancies-prod.bash \
  && ${WORKDIR}/build_frontend-prod.bash \
  && ${WORKDIR}/build_backend.bash \
  && ${WORKDIR}/start.bash
