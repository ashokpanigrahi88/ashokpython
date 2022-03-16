from datetime import datetime
import os
from pathlib import Path
import configparser
import cx_Oracle
import logging

from os import environ
config = configparser.ConfigParser()
config.optionxform = str
config.read('jobhandler/connections.cfg')
DB_CONNECTIONS = config._sections
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ADMIN_SCRIPTS_DIR = os.path.join(BASE_DIR, 'adminscripts')
FROM_DATABASES = ['default']
TO_DATABASES = FROM_DATABASES
DATAHUB = ['default']
DEFAULT_ACTIVE_DB = 'default'
def get_param(p_key, p_db = DEFAULT_ACTIVE_DB):
    val = ""
    try:
        val = DB_CONNECTIONS[p_db][p_key]
        if 'ENV' in val:
            val = os.environ.get(val,'unknown')
    except:
        val = 'unknown'
    finally:
        return val

IMPEXP_USER_ID = 1
TABLE_IGNORE_COLUMNS = ['update_source','created_by','creation_date','last_update_date','last_updated_by']


db_name = DEFAULT_ACTIVE_DB
print('db_name', db_name)
db_dsn = "{}:{}/{}".format(get_param('HOST'),get_param('PORT'),get_param('SID'))
print(db_dsn)
db_connection = cx_Oracle.connect(user=get_param('USER'),password=get_param('PWD_KEY'),dsn=db_dsn)
print('db_connection', db_connection)
def get_cursor(p_connection = db_connection):
    try:
        return p_connection.cursor()
    except Exception as ex:
        print('get cursor',ex)
        return None

if __name__ == '__main__':
    print(db_name, db_connection)

