#!/bin/bash
# This script is used to start PostgreSQL and Apache for edCTF

set -x

# start apache
/usr/sbin/apache2ctl -k restart

# start postgres and display log
sudo -u postgres /usr/lib/postgresql/9.4/bin/postgres -D /var/lib/postgresql/9.4/main -c config_file=/etc/postgresql/9.4/main/postgresql.conf
