#!/usr/bin/env python
"""
Creates a creates an admin user for edctf with default credentials of username 'admin' and password 'admin'.
"""
import os
import sys
import argparse

DESCRIPTION = """
Creates a creates an admin user for edctf with default credentials of username 'admin' and password 'admin'.
"""
EDCTF_DIR = '/opt/edctf'
USERNAME = 'admin'
EMAIL = ''
PASSWORD = 'admin'

if __name__ == "__main__":
    # parse optional arguments
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--path', dest='edctf_dir', default=EDCTF_DIR, help='path containing edctf module (default: {edctf_dir})'.format(edctf_dir=EDCTF_DIR))
    parser.add_argument('--username', dest='username', default=USERNAME, help='admin username (default: {username})'.format(username=USERNAME))
    parser.add_argument('--email', dest='email', default=EMAIL, help='admin email (default: {email})'.format(email=EMAIL))
    parser.add_argument('--password', dest='password', default=PASSWORD, help='admin password (default: {password})'.format(password=PASSWORD))
    args = parser.parse_args()

    # set variables
    edctf_dir = args.edctf_dir
    username = args.username
    email = args.email
    password = args.password

    # append edctf location to path
    sys.path.append(edctf_dir)

    # set edctf settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edctf.settings")
    
    # add admin user
    from django.contrib.auth.models import User
    User.objects.create_superuser(username, email, password)
