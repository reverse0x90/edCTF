#!/bin/bash
# Starts edCTF via apache

# set working directory
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set environment variables for apache
source ${WORKDIR}/environment.bash

# restart/start apache and reload config
sudo -E /usr/sbin/apachectl -k graceful
