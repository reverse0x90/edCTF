#!/bin/bash

sudo /usr/sbin/apache2ctl restart && sudo /usr/sbin/apachectl -k graceful
