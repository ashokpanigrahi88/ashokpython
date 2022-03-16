import os
from os import environ
import logging
from pathlib import Path
from etlhelper import DbParams
from etlhelper import connect, get_rows
from etlhelper.exceptions import ETLHelperError
from datetime import date, datetime, timedelta,timezone, time
from sqlalchemy import create_engine, MetaData
import pandas as pd
import cx_Oracle
import contextvars
import logging
from . import etl_settings

BASE_DIR = Path(__file__).resolve().parent.parent

CURRENT_ACTIVE_DB = contextvars.ContextVar(etl_settings.DEFAULT_ACTIVE_DB)

def set_activedb_name(p_db:str = etl_settings.DEFAULT_ACTIVE_DB ):
   CURRENT_ACTIVE_DB.set(p_db)

def get_activedb_name():
    return CURRENT_ACTIVE_DB.get(etl_settings.DEFAULT_ACTIVE_DB)

def get_db_params(p_db:str = get_activedb_name()):
    print('db param for', p_db)
    dbparam = ""
    v_dbtype = etl_settings.get_param('TYPE',p_db)
    print('dbType',v_dbtype)
    if v_dbtype.upper() == 'ORACLE':
        dbparam =  DbParams(dbtype=v_dbtype,
                            host=etl_settings.get_param('HOST',p_db),
                            port=etl_settings.get_param('PORT',p_db),
                            dbname=etl_settings.get_param('NAME',p_db),
                            user=etl_settings.get_param('USER',p_db)
                            )
        print('dbparam:',dbparam)
        return dbparam

    if v_dbtype.upper() == 'MSSQL':
        dbparam = DbParams(dbtype=v_dbtype,
                           host=etl_settings.get_param('HOST',p_db),
                            port=etl_settings.get_param('PORT',p_db),
                            dbname=etl_settings.get_param('NAME',p_db),
                            user=etl_settings.get_param('USER',p_db),
                            odbc_driver="ODBC Driver 17 for SQL Server")
        ## install odbd drive
        ## enable ssl 3.0 and tls 1.0 in regedit if required
    return dbparam

def get_connection_string(p_db:str , p_type:str ='sqlalchemy'):
    pwdkey = etl_settings.get_param('PWD_KEY',p_db)
    dbparams = get_db_params(p_db)
    try:
        if p_type != 'sqlalchemy':
            return dbparams.get_connection_string(pwdkey)
        else:
            return dbparams.get_sqlalchemy_connection_string(pwdkey)
    except Exception as ex:
        logging.DEBUG(ex)


def get_sqlalchemy_engine(p_db):
    try:
        connstr = get_connection_string(p_db,p_type='sqlalchemy')
        v_connection = create_engine(connstr,max_identifier_length=128, pool_size=20, max_overflow=0)
        return v_connection
    except Exception as ex:
        logging.error('create engine:{}',format(ex))

def get_metadata_engine(p_db:str, p_type:str = 'sqlalchemy'):
    pwdkey = etl_settings.get_param('PWD_KEY',p_db)
    dbparams = get_db_params(p_db)
    connstring = dbparams.get_sqlalchemy_connection_string(pwdkey)
    try:
        metadata = MetaData(connstring)
        return metadata
    except Exception as ex:
        logging.DEBUG(ex)
        return None
""" 
POSTGRESDB = DbParams(dbtype='PG', host="localhost", port=5432,
                      dbname="mydata", user="postgres_user")

SQLITEDB = DbParams(dbtype='SQLITE', filename='/path/to/file.db')

MSSQLDB = DbParams(dbtype='MSSQL', host="localhost", port=1433,
                   dbname="mydata", user="mssql_user",
                   odbc_driver="ODBC Driver 17 for SQL Server")
"""
ROOT_DIRECTORY = BASE_DIR
DIRECTORIES = {
    'exportbase' : os.path.join(ROOT_DIRECTORY,'etl_export\\'),
    'importbase' : os.path.join(ROOT_DIRECTORY,'etl_import\\'),
    'stagebase' : os.path.join(ROOT_DIRECTORY,'etl_stage\\'),
}

DATA_SOURCE_LIST = [{'id':2,'name':get_activedb_name()},]
DATA_TARGET_LIST = DATA_SOURCE_LIST
IMPORT_DEFAULTS ={
    'userid': 1,
    'buid': 1,
    'locationid' : 1,
    'datasource' : 'IMPORT',
}

DEFAULT_JSON_ORIENT = 'records'
sql = "SELECT * FROM dual"

TABLE_SELECT_DICT = {
    'category' : """Select  * from inv_item_categories order by last_update_date""",
}

TABLE_MERGE_DICT = {
    'category' : None
}

def get_ignoredcolumns():
    return etl_settings.TABLE_IGNORE_COLUMNS

def get_directory( p_source ,p_basedir:str = 'exportbase'):
    basedir = DIRECTORIES[p_basedir]
    retval = os.path.join(basedir,p_source+'\\')
    print('basedir',p_basedir, retval)
    return retval

def get_oracledns(p_db:str = 'oratech_datahub'):
    dsn_tns = cx_Oracle.makedsn(etl_settings.get_param('HOST',p_db),
                                etl_settings.get_param('PORT',p_db),
                               sid= etl_settings.get_param('SID',p_db))
    return dsn_tns

def get_raw_connection(p_db:str):
    dsn_tns = get_oracledns(p_db)
    pwdkey = etl_settings.get_param('PWD_KEY',p_db)
    username = etl_settings.get_param('USER',p_db)
    pwd = environ.get(pwdkey)
    connection = cx_Oracle.connect(username, pwd, dsn_tns)
    return connection

def get_timedelta(p_datetime:datetime = datetime.now(), p_deltadays = -1):
    return p_datetime + timedelta(days=p_deltadays)


def get_imp_fromtime(p_dbcolumn, p_type = 'FULL',
                     p_datetime:datetime = datetime.now(),
                     p_deltadays = -1):
    if p_type == 'FULL':
        return " 1 = 1"
    return "{} >= {}".format(p_dbcolumn, p_datetime + timedelta(days=p_deltadays))

def sysdate():
    return datetime.now()

def get_connection(p_db):
    pwdkey = etl_settings.get_param('PWD_KEY',p_db)
    dbparams = get_db_params(p_db)
    print('dbparams',dbparams)
    v_connection = connect(dbparams,pwdkey)
    return v_connection

def is_server_reachable(p_db:str = 'oratech_datahub'):
    dbparams = get_db_params(p_db)
    if not dbparams.is_reachable():
        raise ETLHelperError("network problems connecting to {}".format(p_db))
    return True

def test_connection(p_db:str = 'oratech_datahub',p_sql="select 1 x from dual"):
    pwdkey = etl_settings.get_param('PWD_KEY',p_db)
    try:
        with get_connection(p_db) as conn:
            result = get_rows(p_sql, conn)
        return True
    except Exception as ex:
        print(ex)
        return False

def select_sql(p_selectkey:str = None , p_sql:str = None, p_db:str = 'what_warehoouse'):
    pwdkey = etl_settings.get_param('PWD_KY',p_db)
    v_sql = p_sql
    if p_selectkey:
        v_sql = TABLE_SELECT_DICT[p_selectkey]
    results = None
    with get_connection(p_db) as conn:
        result = get_rows(v_sql, conn)
    return results


def exec_sql(p_connection, p_sql:str = None):
    results = None
    v_sql = p_sql
    with p_connection as conn:
        results = get_rows(v_sql, conn)
    return results


def json_to_csv(p_surce, p_file, p_basedir:str = 'exportbase'):
    sourcedir = get_directory(p_surce,p_basedir=p_basedir)
    sourcefile = "{}{}".format(sourcedir,p_file)
    print('sourcefile',sourcefile)
    df = pd.read_json(sourcefile,orient=DEFAULT_JSON_ORIENT)
    csvfile = "{}{}".format(sourcedir,p_file.replace('.json','.csv'))
    df.to_csv(csvfile)
