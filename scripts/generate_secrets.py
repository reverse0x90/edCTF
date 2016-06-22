#!/usr/bin/env python
"""
Initializes PostgreSQL database and generates Python code containing password and django's secret key.

Run as a user with sudo priveleges.  The outputed Python file will be saved within the edCTF directory for use by settings.py.
"""
from django.utils.crypto import get_random_string
import os
import sys
import string
import argparse


DESCRIPTION = """
Generates Python code containing db password and django's secret key.

Run as a user with sudo priveleges.  The outputed Python file will be saved within the edCTF directory for use by settings.py.
"""
DBPASS = 'edctf'
DBHOST = 'db'
EDCTF_SECRET = '/opt/edctf/edctf/edctf_secret.py'

_CODE_TEMPLATE = """
SECRET_KEY = '{secret}'
DB_PASS = '{dbpass}'
DB_HOST = '{dbhost}'
"""

if __name__ == '__main__':
  # parse optional arguments
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument('--dbhost', dest='dbhost', default=DBPASS, help='database host (default: {dbhost})'.format(dbhost=DBHOST))
  parser.add_argument('--dbpass', dest='dbpass', default=DBPASS, help='database pass (default: {dbpass})'.format(dbpass=DBPASS))
  parser.add_argument('--output', dest='edctf_secret', default=EDCTF_SECRET, help='Python file output location (default: {edctf_secret})'.format(edctf_secret=EDCTF_SECRET))
  args = parser.parse_args()

  dbhost = args.dbhost
  dbpass = args.dbpass
  edctf_secret = args.edctf_secret

  # generate secret
  secret_chars = ''.join(map(chr, range(128)))
  secret = get_random_string(50, secret_chars)

  # Generate python code
  generated_code = _CODE_TEMPLATE.format(
    secret=secret.encode('base64').replace('\n', ''),
    dbpass=dbpass,
    dbhost=dbhost,
  )

  # save secret file
  with open(edctf_secret, 'wb') as f:
    f.write(generated_code)

  # modify access
  os.system('sudo chown "$USER":www-data {edctf_secret} && chmod 750 {edctf_secret}'.format(edctf_secret=edctf_secret))
