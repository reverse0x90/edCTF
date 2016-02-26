from django.core.management import execute_from_command_line
from django.db.utils import ProgrammingError
from django.db import connection
from settings import BASE_DIR
import os
import sys

# import local secrets
try:
  import edctf_secret
except ImportError as err:
  err.message += ".  edctf_secret.py needs to be generated!"
  raise


def run_migrate(ctfname):
  #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
  #execute_from_command_line(['./manage.py', 'migrate', '--database={ctfname}'.format(ctfname=ctfname)])
  os.system('python ./manage.py migrate --database={ctfname}'.format(ctfname=ctfname))

def add_schema(ctfname):
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
  cursor = connection.cursor()
  cursor.execute("CREATE SCHEMA {CTF}".format(CTF=ctfname))

def drop_schema(ctfname):
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
  cursor = connection.cursor()
  cursor.execute("DROP SCHEMA {CTF}".format(CTF=ctfname))

def add_database(ctfname):
  try:
    import edctf_databases
    databases = edctf_databases.databases
  except ImportError:
    databases = {}

  ctfname = str(ctfname)
  if ctfname in databases:
    return False

  databases[ctfname] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'OPTIONS': {
      'options': '-c search_path={CTF}'.format(CTF=ctfname),
    },
    'NAME': '{DB_NAME}'.format(DB_NAME=edctf_secret.DB_NAME),
    'USER': edctf_secret.DB_USER,
    'PASSWORD': edctf_secret.DB_PASSWORD,
    'HOST': edctf_secret.DB_HOST,
    'PORT': edctf_secret.DB_PORT,
  }
  databases = str(databases)

  try:
    add_schema(ctfname)
  except ProgrammingError:
    return False

  with open(os.path.join(BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
    f.write('databases = {databases}\n'.format(databases=databases))

  run_migrate(ctfname)
  return ctfname

def delete_database(ctfname):
  try:
    import edctf_databases
    databases = edctf_databases.databases
  except ImportError:
    databases = {}
    with open(os.path.join(BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
      f.write('databases = {databases}\n'.format(databases=databases))
    return True

  ctfname = str(ctfname)
  if ctfname not in databases:
    return True
  del databases[ctfname]
  databases = str(databases)

  try:
    drop_schema(ctfname)
  except ProgrammingError:
    return True

  with open(os.path.join(BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
    f.write('databases = {databases}\n'.format(databases=databases))

  return ctfname

print add_database('test1')
print add_database('test1')
print delete_database('test1')
print add_database('test1')

