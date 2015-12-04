#!/bin/bash

# set working directory
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set environment variables
source ${WORKDIR}/environment.bash

# run scripts
${WORKDIR}/install_dependancies.bash \
  && ${WORKDIR}/build_frontend.bash \
  && ${WORKDIR}/build_backend.bash \
  && ${WORKDIR}/start.bash
