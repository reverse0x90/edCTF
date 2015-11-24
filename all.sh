#!/bin/sh

export EDCTF_DIR=/opt/edctf

/bin/sh ${EDCTF_DIR}/prepare.sh \
  && /bin/sh ${EDCTF_DIR}/build.sh \
  && /bin/sh ${EDCTF_DIR}/run.sh
