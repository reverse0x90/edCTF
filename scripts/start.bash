#!/bin/bash

/usr/sbin/apache2ctl restart && /usr/sbin/apachectl -k graceful
