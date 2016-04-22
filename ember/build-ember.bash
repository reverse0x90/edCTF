#!/bin/bash

USAGE="Usage: $(basename "$0") [OPTIONS]

Builds ember for edctf.

Options:
    -p  build for production
    -d  build for development
    -h  display help
"

DEV=false
PROD=false

OPTIND=1
while getopts "pdh" opt; do
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
    esac
done

if $DEV && $PROD; then
  echo "Cannot build for both production and development!" 1>&2
  exit 1
fi

if $DEV; then
  ember build --output-path /opt/edctf/edctf/static/ember
else
  if $PROD; then
    ember build --environment=production --output-path /opt/edctf/edctf/static/ember
  else
    echo "Give a flag for environment!!!" 1>&2
    echo
    echo -e "$USAGE"
    exit 1
  fi
fi
