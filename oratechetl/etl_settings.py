import oratechetl.secrets

import os
from os import environ
from pathlib import Path
import configparser
config = configparser.ConfigParser()
config.optionxform = str
config.read('etlconnections.cfg')
DB_CONNECTIONS = config._sections
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ADMIN_SCRIPTS_DIR = os.path.join(BASE_DIR, 'adminscripts')
FROM_DATABASES = ['what_warehouse']
TO_DATABASES = FROM_DATABASES
DATAHUB = ['oratech_datahub']
DEFAULT_ACTIVE_DB = 'oratech_datahub'
def get_param(p_key, p_db = DEFAULT_ACTIVE_DB):
    return DB_CONNECTIONS[p_db][p_key]
IMPEXP_USER_ID = 1
TABLE_IGNORE_COLUMNS = ['update_source','created_by','creation_date','last_update_date','last_updated_by']
