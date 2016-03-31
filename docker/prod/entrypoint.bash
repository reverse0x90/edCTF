#!/bin/bash
set -x

# Start services
/etc/init.d/postgresql start && /usr/sbin/apache2ctl -k restart

# Entrypoint
/bin/bash
