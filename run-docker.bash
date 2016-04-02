#!/bin/bash

SCRIPTS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/scripts
. ${SCRIPTS}/environment.bash

DEV=false
PROD=false
LOCAL=false

OPTIND=1
while getopts "dpl" opt; do
    case $opt in
        d)
          DEV=true
          ;;
        p)
          PROD=true
          ;;
        l)
          LOCAL=true
          ;;
    esac
done
if $DEV && $PROD; then
  echo "Cannot build for both production and development!" 1>&2
  exit 1
fi

if $DEV; then
  UUID=`id -u`
  echo "Creating development container..."
  set -x
  docker build -t edctf:dev -f ${EDCTF_DOCKER}/dev/Dockerfile ${EDCTF_DIR} \
    && docker run --name edctf_db_dev \
      -e POSTGRES_USER=edctf -e POSTGRES_PASSWORD=edctf \
      -d postgres \
    && docker run --restart=unless-stopped --link edctf_db_dev:db \
      -e UUID=$UUID -e USER=$USER \
      -v ${EDCTF_DIR}:/opt/edctf \
      -p 8080:80 -p 4443:443 \
      -it edctf:dev
else
  echo "Creating production container..."
  set -x
  docker build -t edctf:prod ${EDCTF_DIR} \
    && docker run --name edctf_db \
      -e POSTGRES_USER=edctf -e POSTGRES_PASSWORD=edctf \
      -d postgres \
    && docker run --restart=unless-stopped --name=edctf_server --link edctf_db:db \
      -p 80:80 -p 443:443 \
      -d edctf:prod
fi
