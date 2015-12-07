#!/bin/bash
# This script is used to start PostgreSQL and Apache for edCTF

# start apache
/usr/sbin/apache2ctl -k restart

# start postgres and display log
sudo -u postgres /usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf
