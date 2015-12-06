#!/bin/bash

# set working directory
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# set environment variables
source ${WORKDIR}/environment.bash

# set temporary envvars
export TEMP_ENVVARS="/tmp/edctfenvvars"

# add default envars
cat ${EDCTF_CONFIG}/envvars > ${TEMP_ENVVARS}

# add edCTF envvars
echo >> ${TEMP_ENVVARS}
echo "# edCTF environment variables" >> ${TEMP_ENVVARS}

# set edCTF root
echo export EDCTF_DIR=${EDCTF_DIR} >> ${TEMP_ENVVARS}

# set subdirectory
echo export EDCTF_DJANGO=${EDCTF_DJANGO} >> ${TEMP_ENVVARS}

# set static directory
echo export EDCTF_STATIC=${EDCTF_STATIC} >> ${TEMP_ENVVARS}

# set favicon path
echo export EDCTF_FAVICON=${EDCTF_FAVICON} >> ${TEMP_ENVVARS}

# set apache log paths
echo export EDCTF_ERROR_LOG=${EDCTF_ERROR_LOG} >> ${TEMP_ENVVARS}
echo export EDCTF_ACCESS_LOG=${EDCTF_ACCESS_LOG} >> ${TEMP_ENVVARS}

echo >> ${TEMP_ENVVARS}

# Backup current envvars
sudo mv ${APACHE_ENVVARS}{,.backup-`date +%s`}

# set new envvars
sudo cp ${TEMP_ENVVARS} ${APACHE_ENVVARS}

# remove temp envvars
rm ${TEMP_ENVVARS}
