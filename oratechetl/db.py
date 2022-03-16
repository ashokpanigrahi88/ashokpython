from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session, mapper
from sqlalchemy import MetaData,Column, String, Integer, Table, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
import logging

from sqlalchemy import create_engine
import oratechetl.utilconfig as utilconfig

db_name = utilconfig.get_activedb_name()
print('db_name', db_name)
db_engine = utilconfig.get_sqlalchemy_engine(db_name)
db_metadata = MetaData(bind=db_engine)
db_session  = scoped_session(sessionmaker(bind=db_engine))

print('session', db_session)
db_connection = utilconfig.get_connection(db_name)
print('db_connection', db_connection)
db_raw_connection = utilconfig.get_raw_connection(db_name)
# automap base
db_automapbase = automap_base()
db_declarativebase = declarative_base(bind=db_engine)

def get_TableObject(p_table, p_meta=db_metadata):
    try:
        return Table(p_table, p_meta, autoload=True)
    except Exception as ex:
        logging.error(ex)


def get_mapperClass(p_class , p_table, p_meta=db_metadata):
    try:
        table = get_TableObject(p_table,p_meta=p_meta)
        mapped = mapper(p_class,table)
        return p_class
    except Exception as ex:
        logging.error(ex)

if __name__ == '__main__':
    print(db_name, db_engine, db_session)

