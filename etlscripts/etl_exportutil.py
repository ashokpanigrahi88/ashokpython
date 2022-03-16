import os
import pandas as pd
import logging
from etlhelper import execute
from oratechetl import (utilconfig, commonutil, etl_settings)
from oratechetl import imp_exp_settings as impexp

def export_data_to_file( p_connection,
                        p_table:str = 'ALL',
                        p_source:str = 'what_warehouse',
                        p_datasource:str = None,
                        p_filedirectory:str = 'exportbase',
                        p_file:bool = True,
                        p_additionalwhere:str = "",
                        p_outputformat:str = 'json'
                      ):
    v_source = impexp.DATA_IMPORT_SOURCE[p_source]
    logging.info('export_data_to_file:{}'.format(p_filedirectory))
    datasource = commonutil.nvl(p_datasource,p_source)
    df = pd.DataFrame()
    if os.path.isdir(p_filedirectory) or ':' in p_filedirectory:
        file_directory = p_filedirectory
    else:
        file_directory =  utilconfig.get_directory(p_source=p_source, p_basedir=p_filedirectory)
    for i in v_source.keys():
        if p_table == 'ALL' or p_table  in i:
            tablename, columns, where, orderby,file, indexcol = v_source[i]
            print('indexcol',indexcol)
            if len(indexcol) > 0:
                if len(tablename) <= 1:
                    v_sql = columns
                else:
                    v_sql = """SELECT {}, '{}' third_party_source, {} third_party_source_ref
                                    FROM {} 
                                    WHERE {} {}
                                    ORDER BY {}""".format(columns,
                                                          datasource,
                                                          indexcol,
                                                          tablename,where,p_additionalwhere,orderby)
                print(v_sql)
                try:
                    df = pd.read_sql(v_sql, con=p_connection)
                    if p_file:
                        if p_outputformat ==  'json':
                            df.to_json(file_directory + file, orient=impexp.DEFAULT_JSON_ORIENT)
                        else:
                            df.to_csv(file_directory + file.replace('json','csv'))
                    logging.info('exported:{}'.format(file))
                except Exception as ex:
                    print(ex)
                    logging.error('exported:{}'.format(file))

    return df

def pull_remote_data( p_connection,
                        p_table:str = 'ALL',
                        p_source:str = 'what_warehouse',
                        p_filedirectory:str = 'importbase',
                        p_file:bool = True,
                        p_additionalwhere:str = ""
                      ):
    v_source = impexp.DATA_IMPORT_SOURCE[p_source]
    if not os.path.isdir(p_filedirectory):
        file_directory =  utilconfig.get_directory(p_source=p_source, p_basedir=p_filedirectory)
    else:
        file_directory = p_filedirectory
    for i in v_source.keys():
        if p_table == 'ALL' or p_table  == i:
            tablename, columns, where, orderby,file, indexcol = v_source[i]
            if len(indexcol) > 0:
                v_sql = """ {}, '{}' third_party_source, {} third_party_source_ref
                               {} 
                                 {} {}
                                 {}""".format(columns,
                                                      p_source,
                                                      indexcol,
                                                      tablename,where,p_additionalwhere,orderby)
                df = pd.read_sql(v_sql, con=p_connection)
                df.columns = map(str.lower, df.columns)
                if p_file:
                    df.to_json(file_directory + file, orient=impexp.DEFAULT_JSON_ORIENT)
    if p_table == 'ALL' or p_table == 'qtyinstock':
        df = impexp.export_qtyinstock(p_connection)
        file = 'qtyinstock.json'
        if p_file:
            df.to_json(file_directory+file,orient=impexp.DEFAULT_JSON_ORIENT)
    return df



def export_data(p_db,p_table:str = 'ALL', p_outputformat:str = 'json'):
    conn = utilconfig.get_connection(p_db)
    sourcealias = etl_settings.get_param('ALIAS', p_db)
    file_directory = utilconfig.get_directory(p_source=sourcealias)
    data = export_data_to_file(p_connection=conn,p_source=sourcealias,
                        p_table=p_table,p_filedirectory=file_directory, p_outputformat=p_outputformat)




def export_data_for(p_source,p_target,p_table:str = 'ALL', p_outputformat:str = 'json', p_targettype:str='file'):
    conn = utilconfig.get_connection(p_source)
    targetalias = etl_settings.get_param('ALIAS', p_target)
    file_directory = utilconfig.get_directory(p_source=targetalias)
    data = export_data_to_file(p_connection=conn,p_source=p_target,p_datasource=p_source,
                        p_table=p_table,p_filedirectory=file_directory, p_outputformat=p_outputformat)