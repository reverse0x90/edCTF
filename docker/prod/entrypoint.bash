#!/bin/bash
set -x

# Start services
#/etc/init.d/postgresql start && /usr/sbin/apache2ctl -k restart
/etc/init.d/postgresql start

# Entrypoint
#sudo -u postgres /usr/lib/postgresql/9.4/bin/postgres -D /var/lib/postgresql/9.4/main -c config_file=/etc/postgresql/9.4/main/postgresql.conf
/usr/sbin/apache2ctl -D FOREGROUND
