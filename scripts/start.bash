#!/bin/bash
# Starts edCTF via apache

# restart/start apache and reload config
sudo /usr/sbin/apachectl -k graceful
