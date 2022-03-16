from sqlalchemy import (MetaData, create_engine, select, insert, inspect,
                        delete, update, Unicode, Column, VARCHAR,Numeric,ForeignKey)
from datetime import datetime, date
from oratechetl import utilconfig as utilconfig


def get_instance(p_class,p_table):
    return mapper
