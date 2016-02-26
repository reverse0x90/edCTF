from django.conf import settings
from django.db.utils import ProgrammingError
from django.db import connection
from time import time
from random import randint
import os
import sys

# import local secrets
try:
  import edctf_secret
except ImportError as err:
  err.message += ".  edctf_secret.py needs to be generated!"
  raise


def _run_migrate(ctfname):
  """
  Runs django migrate database command
  """
  sys.path.append(settings.BASE_DIR)
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
  from django.core.management import execute_from_command_line
  execute_from_command_line([os.path.join(settings.BASE_DIR, 'manage.py'), 'migrate', '--database={ctfname}'.format(ctfname=ctfname)])

def _add_schema(ctfname):
  """
  Adds ctf schema to database
  """
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
  cursor = connection.cursor()
  cursor.execute("CREATE SCHEMA {CTF}".format(CTF=ctfname))

def _drop_schema(ctfname):
  """
  Drops ctf schema from database
  """
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
  cursor = connection.cursor()
  cursor.execute("DROP SCHEMA {CTF} CASCADE".format(CTF=ctfname))

def add_ctf(ctf_id=None, ctfname=None):
  """
  Creates the new schema for given ctf_id and adds it to settings
  Returns with schema name on success, False otherwise
  """
  try:
    import edctf_databases
    databases = edctf_databases.databases
  except ImportError:
    databases = {}
  
  if ctf_id != None:
    ctfname = 'ctf_{id}'.format(id=str(ctf_id))
  elif ctfname != None:
    ctfname = str(ctfname)
  else:
    raise ValueError("ctf_id or ctfname must be given!")

  if ctfname in databases:
    return "in the database already!"
    return False

  databases[ctfname] = {
    'OPTIONS': {
      'options': '-c search_path={CTF}'.format(CTF=ctfname),
    },
  }
  str_databases = str(databases)

  try:
    _add_schema(ctfname)
  except ProgrammingError:
    raise
    return False

  with open(os.path.join(settings.BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
    f.write('databases = {databases}\n'.format(databases=str_databases))
  
  # force settings to update
  try:
    settings.DATABASES[ctfname] = {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'OPTIONS': databases[ctfname]['OPTIONS'],
      'NAME': edctf_secret.DB_NAME,
      'USER': edctf_secret.DB_USER,
      'PASSWORD': edctf_secret.DB_PASSWORD,
      'HOST': edctf_secret.DB_HOST,
      'PORT': edctf_secret.DB_PORT,
    }
  except KeyError:
    pass

  _run_migrate(ctfname)
  return ctfname

def delete_ctf(ctf_id=None, ctfname=None):
  """
  Deletes the ctf schema for given ctf_id and removes it from settings
  Returns with schema name on success, otherwise returns False
  """
  try:
    import edctf_databases
    databases = edctf_databases.databases
  except ImportError:
    databases = {}
    with open(os.path.join(settings.BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
      f.write('databases = {databases}\n'.format(databases=databases))
    return False

  if ctf_id != None:
    ctfname = 'ctf_{id}'.format(id=str(ctf_id))
  elif ctfname != None:
    ctfname = str(ctfname)
  else:
    raise ValueError("ctf_id or ctfname must be given!")

  if ctfname not in databases:
    try:
      _drop_schema(ctfname)
      return False
    except ProgrammingError:
      return False

  try:
    _drop_schema(ctfname)
  except ProgrammingError:
    del databases[ctfname]
    databases = str(databases)
    with open(os.path.join(settings.BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
      f.write('databases = {databases}\n'.format(databases=databases))
    import edctf_databases
    return False

  del databases[ctfname]
  str_databases = str(databases)
  with open(os.path.join(settings.BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
    f.write('databases = {databases}\n'.format(databases=str_databases))
  
  # force settings to update
  try:
    del settings.DATABASES[ctfname]
  except KeyError:
    return False
  
  return ctfname

def delete_all_ctfs():
  """
  Deletes all ctf schemas
  """
  try:
    import edctf_databases
    databases = edctf_databases.databases
  except ImportError:
    databases = {}
    with open(os.path.join(settings.BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
      f.write('databases = {databases}\n'.format(databases=databases))
    return True
  
  keys = [key for key in databases]
  for key in keys:
    try:
      delete_ctf(ctfname=key)
    except:
      raise
      continue
  
  with open(os.path.join(settings.BASE_DIR, 'edctf/edctf_databases.py'), 'wb') as f:
    f.write('databases = {databases}\n'.format(databases=databases))
  return True

def get_uid():
  """
  Returns the next id for a valid schema id
  """
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
  cursor = connection.cursor()
  cursor.execute("select schema_name from information_schema.schemata where schema_name like 'ctf_%'")
  schemas = cursor.fetchall()
  
  ctfs = [schema[0] for schema in schemas]
  i = 0
  while 1:
    attempt = 'ctf_' + str(i)
    if attempt not in ctfs:
      return i
    i += 1
