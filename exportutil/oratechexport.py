#!/usr/bin/env python
# coding: utf-8
#pip install cx_oracle
import time
from datetime import datetime
import os
import sys
import cx_Oracle
import dbconfig as cn_config
import exportschema as cn_export
DSN_TNS = ""
CONNECTION = ""

def get_connection():
    if cn_config.DB_PASSWORD == '-1' or cn_config.DB_SERVER == '-1' or cn_config.DB_USERNAME == '-1':
        print('Cannot connect to database')
        return None
    try:
        DSN_TNS = cx_Oracle.makedsn(cn_config.DB_SERVER, cn_config.DB_PORT, cn_config.DB_SID)
        CONNECTION = cx_Oracle.connect(cn_config.DB_USERNAME, cn_config.DB_PASSWORD, DSN_TNS)
        return CONNECTION
    except Exception as ex:
        print(ex)
        return  None

#instock_df = export_qtyinstock(connection)
#instock_df_original = instock_df.copy()
#instock_df.DERIVED_SALESUNIT = instock_df.DERIVED_SALESUNIT.replace({0:1})
#instock_df.DERIVED_SALESUNIT

def exportdata(p_type = 'TABLES', p_frequency=60*60):
    connection = get_connection()
    if connection is None:
        print('Cannot export data')
        exit(-1)
    while True:
        cn_export.export_data_to_json(connection,p_type)
        print('time:', datetime.now() )
        if p_frequency == -1:
            break;
        print('Sleeping {} seconds'.format(p_frequency))
        time.sleep(p_frequency)
        print('Woken up')


def exportqtyinstock(p_type = 'QTYINSTOCK', p_frequency=60*5):
    connection = get_connection()
    if connection is None:
        print('Cannot export data')
        exit(-1)
    while True:
        cn_export.export_data_to_json(connection,p_type)
        print('time:',datetime.now())
        if p_frequency == -1:
            break;
        print('Sleeping {} seconds'.format(p_frequency))
        time.sleep(p_frequency)
        print('Woken up')
