#!/bin/bash

export SCRIPTS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/scripts
. "${SCRIPTS}/environment.bash"

RED='\033[0;31m'
NC='\033[0m'
USAGE="Usage: $(basename "$0") [OPTIONS]

Deploys the edctf framework.
By default, uses Docker containers to run Apache and PostgreSQL.

Options:
    -h  display help text
    -p  use production environment [DEFAULT]
    -d  use development environment
    -l  run edctf locally instead of within a Docker container

Examples:
    $(basename "$0")
        - runs edctf

    $(basename "$0") -l
        - runs edctf locally

    $(basename "$0") -d
        - runs edctf within a development container
"
CHECKINSTALLED="docker ps"
NOTINSTALLED="
${RED}Cannot run docker${NC}

Please install docker or install locally (-l) within an ubuntu environment.
Docker installation instructions: https://docs.docker.com/engine/installation/
"

DEV=false
PROD=false
LOCAL=false

OPTIND=1
while getopts "hpdl" opt; do
    case $opt in
        h)
          echo -e "$USAGE"
          exit
          ;;
        p)
          PROD=true
          ;;
        d)
          DEV=true
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

if ! $LOCAL; then
  `$CHECKINSTALLED > /dev/null`
  if [ $? -ne 0 ]; then
    echo -e "$NOTINSTALLED"
    exit 1
  fi
  
  if $DEV; then
    DB_PASS=edctf
    DB_HOST=db
    UUID=`id -u`

    echo "Building development container..."
    docker build -t edctf:dev -f "${EDCTF_DOCKER}/dev/Dockerfile" "${EDCTF_DIR}" \
      && docker run --name edctf_db_dev \
        -e POSTGRES_DB=edctf -e POSTGRES_USER=edctf \
        -e POSTGRES_PASSWORD="${DB_PASS}" \
        -d postgres \
      && docker run --restart=unless-stopped --link edctf_db_dev:"${DB_HOST}" \
        -e UUID="$UUID" -e USER="$USER" \
        -e DB_PASS="${DB_PASS}" -e DB_HOST="${DB_HOST}" \
        -v "${EDCTF_DIR}":/opt/edctf \
        -p 8080:80 -p 4443:443 -p 4200:4200 \
        -it edctf:dev
  else
    DB_PASS=edctf
    DB_HOST=db

    echo "Building production container..."
    docker build -t edctf:prod "${EDCTF_DIR}" \
      && docker run --name edctf_db \
        -e POSTGRES_DB=edctf -e POSTGRES_USER=edctf \
        -e POSTGRES_PASSWORD="${DB_PASS}" \
        -d postgres \
      && docker run --restart=unless-stopped --name=edctf_server --link edctf_db:"${DB_HOST}" \
        -e DB_PASS="${DB_PASS}" -e DB_HOST="${DB_HOST}" \
        -p 80:80 -p 443:443 \
        -d edctf:prod
  fi
else
  if $DEV; then
    export DB_PASS=edctf
    export DB_HOST=localhost

    echo "Creating development environment locally..."
    set -x
    "${SCRIPTS}/development.bash"
  else
    export DB_PASS=edctf
    export DB_HOST=localhost

    echo "Creating production environment locally..."
    set -x
    "${SCRIPTS}/production.bash"
  fi
fi