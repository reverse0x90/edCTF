#!/bin/bash

SCRIPTS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/scripts
. ${SCRIPTS}/environment.bash

DEV=false
PROD=false

OPTIND=1
while getopts ':pd' opt
do
    case "$opt" in
        d)
          DEV=true;break
          ;;
        p)
          PROD=true;break
          ;;
    esac
done


if $DEV; then
  echo "Creating development container..."
  set -x
  docker build -t edctf:dev -f ${EDCTF_DOCKER}/dev/Dockerfile ${EDCTF_DIR} \
    && docker run -it --restart=unless-stopped -v ${EDCTF_DIR}:/opt/edctf edctf:dev
else
  echo "Creating production container..."
  set -x
  docker build -t edctf:prod -f ${EDCTF_DOCKER}/prod/Dockerfile ${EDCTF_DIR} \
    && docker run --restart=unless-stopped -p 80:80 -p 443:443 --name=edctf_server -d edctf:prod
fi
