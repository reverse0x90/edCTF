#!/bin/bash
# Sets environment variables relating to edCTF

# set edCTF root
export EDCTF_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# set subdirectories
export EDCTF_EMBER="${EDCTF_DIR}/ember"
export EDCTF_DJANGO="${EDCTF_DIR}/edctf"
export EDCTF_SCRIPTS="${EDCTF_DIR}/scripts"
export EDCTF_CONFIG_HTTP="${EDCTF_DIR}/config/http"
export EDCTF_CONFIG_HTTPS="${EDCTF_DIR}/config/https"

# set static directories
export EDCTF_STATIC="${EDCTF_DJANGO}/static"
export EDCTF_EMBER_STATIC="${EDCTF_STATIC}/ember"
export EDCTF_ADMIN_STATIC="${EDCTF_STATIC}/admin"
export EDCTF_REST_STATIC="${EDCTF_STATIC}/rest_framework"

# set favicon path
export EDCTF_FAVICON="${EDCTF_STATIC}/icons/favicon.ico"

# set dependancy paths
export APACHE_CONFIG="/etc/apache2/sites-enabled"
export APACHE_ENVVARS="/etc/apache2/envvars"
export DJANGO_ADMIN_STATIC="/usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin"
export REST_FRAMEWORK_CSS_DIR="/usr/local/lib/python2.7/dist-packages/rest_framework/static/rest_framework"


# set database information
export EDCTF_DATABASE="edctf"

# set apache log paths
export EDCTF_ERROR_LOG="/var/log/edctf-error.log"
export EDCTF_ACCESS_LOG="/var/log/edctf-access.log"

# set apache ssl settings
# currently installs and generates a self-signed cert when ssl is set to true
export USE_SSL="false"
export SSL_DIR="/etc/apache2/ssl"
export SSL_COUNTRY="US"
export SSL_STATE="NA"
export SSL_LOCALITY="NA"
export SSL_ORGANIZATION="NA"
export SSL_OU="NA"
export SSL_CN="example.com"
