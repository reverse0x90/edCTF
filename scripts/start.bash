#!/bin/bash
# Starts edCTF via apache

# restart/start apache and reload config
sudo apache2ctl graceful-stop 2&>/dev/null
sudo apache2ctl start
