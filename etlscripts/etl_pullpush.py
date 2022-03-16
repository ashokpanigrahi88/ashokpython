import os
import pandas as pd
from oratechetl import (utilconfig,  dbfuncs)
from oratechetl import imp_exp_settings as impexp
import logging

def pull_remote_data( p_connection = None,
                        p_table:str = 'ALL',
                        p_source:str = 'what_warehouse',
                        p_filedirectory:str = 'importbase',
                        p_file:bool = True,
                        p_additionalwhere:str = "",
                        p_filextension = 'json',
                        p_db = ""
                      ):
    if len(p_db) > 0:
        p_connection = utilconfig.get_connection(p_db)
    else:
        if not p_connection:
            p_connection = utilconfig.get_connection(p_source)
    logging.debug(f'pulling data:{p_table} from {p_source} directory {p_filedirectory}')
    v_source = impexp.DATA_IMPORT_SOURCE[p_source]
    if not os.path.isdir(p_filedirectory):
        file_directory =  utilconfig.get_directory(p_source=p_source, p_basedir=p_filedirectory)
    else:
        file_directory = p_filedirectory
    for i in v_source.keys():
        if p_table == 'ALL' or p_table  == i:
            tablename, columns, where, orderby,file, indexcol = v_source[i]
            file = file.replace('json',p_filextension)
            if len(indexcol) > 0:
                if len(tablename) > 0:
                    v_sql = """SELECT {}, '{}' third_party_source, {} third_party_source_ref
                                    FROM {} 
                                    WHERE {} {}
                                    ORDER BY {}""".format(columns,
                                                          p_source,
                                                          indexcol,
                                                          tablename,where,p_additionalwhere,orderby)
                else:
                    v_sql = columns
                df = pd.read_sql(v_sql, con=p_connection)
                df.columns = map(str.lower, df.columns)
                if p_file:
                    if p_filextension == 'json':
                        df.to_json(file_directory + file, orient=impexp.DEFAULT_JSON_ORIENT)
                    else:
                        df.to_csv(file_directory + file)
    return df

