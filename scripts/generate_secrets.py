#!/usr/bin/env python
"""
Initializes PostgreSQL database and generates Python code containing password and django\'s secret key.

Run as a user with sudo priveleges.  The outputed Python file will be saved within the edCTF directory for use by settings.py.
"""
from django.utils.crypto import get_random_string
import os
import sys
import string
import argparse


DESCRIPTION = """
Initializes PostgreSQL database and generates Python code containing password and django\'s secret key.

Run as a user with sudo priveleges.  The outputed Python file will be saved within the edCTF directory for use by settings.py.
"""
DBNAME = 'edctf'
DBUSER = 'edctf'
DBHOST = 'localhost'
DBPORT = ''
EDCTF_SECRET = '/opt/edctf/edctf/edctf_secret.py'

_CODE_TEMPLATE = """
# Django secret key
SECRET_KEY = '{secret}'

# PostgreSQL information
DB_NAME = '{dbname}'
DB_USER = '{dbuser}'
DB_PASSWORD = '{dbpassword}'
DB_HOST = '{dbhost}'
DB_PORT = '{dbport}'
"""
_POSTGRES_TEMPLATE = """(sudo -u postgres psql -c "CREATE USER {dbuser} WITH PASSWORD '{dbpassword}';") \\
  || (sudo -u postgres psql -c "ALTER USER {dbuser} WITH PASSWORD '{dbpassword}';"); \\
sudo -u postgres psql -c "CREATE DATABASE {dbname};"; \\
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {dbname} to {dbuser};";
"""

if __name__ == '__main__':
    # parse optional arguments
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--dbname', dest='dbname', default=DBNAME, help='database name (default: {dbname})'.format(dbname=DBNAME))
    parser.add_argument('--dbuser', dest='dbuser', default=DBUSER, help='database user (default: {dbuser})'.format(dbuser=DBUSER))
    parser.add_argument('--dbhost', dest='dbhost', default=DBHOST, help='database host (default: {dbhost})'.format(dbhost=DBHOST))
    parser.add_argument('--dbport', dest='dbport', default=DBPORT, help='database port (default: {dbport})'.format(dbport=DBPORT))
    parser.add_argument('--output', dest='edctf_secret', default=EDCTF_SECRET, help='Python file output location (default: {edctf_secret})'.format(edctf_secret=EDCTF_SECRET))
    args = parser.parse_args()

    # set secret and password character sets
    secret_chars = ''.join(map(chr, range(128)))
    password_chars = string.ascii_letters + string.digits
    
    # generate new django secret
    secret = get_random_string(50, secret_chars)
    
    # set database information
    dbname = args.dbname
    dbuser = args.dbuser
    dbpassword = get_random_string(50, password_chars)
    dbhost = args.dbhost
    dbport = args.dbport

    # set output file
    edctf_secret = args.edctf_secret

    # setup database
    postgres_setup = _POSTGRES_TEMPLATE.format(
        dbname = dbname,
        dbuser = dbuser,
        dbpassword = dbpassword,
    )
    os.system(postgres_setup)

    # generate secret file
    generated_code = _CODE_TEMPLATE.format(
        secret = secret.encode('base64').replace('\n',''),
        dbname = dbname,
        dbuser = dbuser,
        dbpassword = dbpassword,
        dbhost = dbhost,
        dbport = dbport,
    )

    # save secret file
    with open(edctf_secret, 'wb') as f:
        f.write(generated_code)

    # modify access, since running as escalated user
    os.system('chmod 755 {edctf_secret}'.format(edctf_secret=edctf_secret))
