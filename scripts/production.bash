#!/bin/bash
# Runs install, build, and run scripts to start within a production environment

# set working directory
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set environment variables
source ${WORKDIR}/environment.bash

# run scripts
${WORKDIR}/install_dependancies-prod.bash \
  && ${WORKDIR}/build_frontend-prod.bash \
  && ${WORKDIR}/build_backend.bash \
  && ${WORKDIR}/start.bash
