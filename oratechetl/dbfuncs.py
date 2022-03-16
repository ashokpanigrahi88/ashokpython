from random import random
from datetime import date , datetime
from oratechetl import (etl_settings, commonutil, db, utilconfig, dateutil)
from crudapi import generic
from oratechetl.model import (CmnUsers)
from oratechetl import OratechExceptions as myex
import cx_Oracle
import logging

DB_NAME = db.db_name
connection = utilconfig.get_raw_connection(DB_NAME)


def get_sequenceval(p_sequence,cursor = connection.cursor() ,p_close:bool = False):
    val = None
    try:
        cursor.execute("SELECT "  + p_sequence +" val From Dual")
        row = cursor.fetchone()
        val = row[0]
    except Exception as ex:
        logging.error("{} {}".format(p_sequence, ex))
    finally:
        if p_close:
            cursor.close()
        return val

def random_string():
    return str(random.randint(1, 99999999))

def insert_record(p_table:str, p_columns:str,p_values:str ,cursor = connection.cursor() ,p_close:bool = False):
    val = None
    try:
        sql = """ INSERT INTO {} ( {} )""".format(p_table,p_columns)
        if type(p_values) != str:
            sql += """ VALUES {} """.format(p_values)
        else:
            sql += p_values
        cursor.execute(sql)
        connection.commit()
    except Exception as ex:
        print(ex)
        logging.error("insert {} - {}".format(p_table, ex))
    finally:
        if p_close:
            cursor.close()


def insert_fromdict(p_table:str, p_data:{} = {},cursor = connection.cursor() ,p_close:bool = False):
    try:
        columns = ""
        values = ""
        if p_data == {}:
            logging.debug('insert_fromdict blank or invalid data')
            return
        for key, value in p_data.items():
            if len(columns) > 0:
                columns += ', '
                values += ', '
            columns += '{}'.format(key)
            print(type(value))
            if type(value) == str:
                if value == 'sysdate' or value.startswith('TO_DATE'):
                    values += "{}".format(value)
                else:
                    values += "'{}'".format(value)
            elif type(value) == datetime:
                values += "{}".format(dateutil.datetimeto_oracle(value))
            else:
                values += "{}".format(value)
        values = " VALUES (" + values + ")"
        insert_record(p_table=p_table, p_columns=columns, p_values=values)
    except Exception as ex:
        print(ex)
        logging.error(ex)
    finally:
        if p_close:
            cursor.close()

def update_record(p_table:str, p_setcolumns ,p_where ,cursor = connection.cursor() ,p_close:bool = False):
    try:
        sql = """ UPDATE {} set  {} 
                WHERE ({}""".format(p_table, p_setcolumns,p_where)
        cursor.execute(sql)
        connection.commit()
    except Exception as ex:
        logging.error("update {} - {}".format(p_table, ex))
    finally:
        if p_close:
            cursor.close()

def delete_record(p_table:str,p_where ,cursor = connection.cursor() ,p_close:bool = False):
    try:
        sql = """ Delete {} 
                WHERE ({}""".format(p_table,p_where)
        cursor.execute(sql)
        connection.commit()
    except Exception as ex:
        logging.error("delete {} - {}".format(p_table, ex))
    finally:
        if p_close:
            cursor.close()


def dml(p_table:str,p_sql ,cursor = connection.cursor() ,p_close:bool = False):
    try:
        sql = p_sql.format(p_table)
        connection.commit()
    except Exception as ex:
        logging.error("dml{} - {}".format(sql, ex))
    finally:
        if p_close:
            cursor.close()

def systemlog(p_msg , p_name, p_type='SYSTEM',cursor = connection.cursor() ,p_close:bool = False):
    try:
        columns = "log_description, log_name, log_type, log_date"
        values = """ VALUES ('{}', '{}', '{}', {} )""".format(p_msg, p_name, p_type, dateutil.get_oracledatetime())
        table = 'sys_log_headers'
        insert_record(p_table=table,p_columns=columns,p_values=values,cursor=cursor, p_close=False)
    except:
        pass
    finally:
        if p_close:
            cursor.close()


def allrowsto_dict(cursor,columnscase:str = 'lower'):
    "Return all rows from a cursor as a dict"
    if columnscase == 'lower':
        columns = [col[0].lower() for col in cursor.description]
    else:
        columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def rowto_dict(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_fuzzysearch(fuzzyword:str ,cursor = connection.cursor() ,p_close:bool = False,**kwargs):
    val = None
    try:
        val = cursor.callfunc("Inv_Pkg.item_FuzzySearch", str, [fuzzyword])
    except:
        pass
    finally:
        if p_close:
            cursor.close()
        return val


def exec_int_func(funcame:str, param:[] ,cursor = connection.cursor() ,p_close:bool = False, **kwargs):
    #cursor.callproc("so_test", keywordParameters = dict(p2 = "Y", p3 = "Z"))
    val = None
    try:
        if kwargs:
            val = cursor.callfunc(funcame, int, keywordParameters = kwargs)
        else:
            val = cursor.callfunc(funcame, int, param)
    except Exception as ex:
        print(ex)
        raise myex.UnhandledError(ex)
    finally:
        if p_close:
            cursor.close()
        return val

def exec_str_func(funcame:str, param:[], cursor = connection.cursor() ,p_close:bool = False , **kwargs):
    #cursor.callproc("so_test", keywordParameters = dict(p2 = "Y", p3 = "Z"))
    val = None
    try:
        if kwargs:
            val = cursor.callfunc(funcame, str, keywordParameters=kwargs)
        else:
            val = cursor.callfunc(funcame, str, param)
    except Exception as ex:
        raise myex.UnhandledError(ex)
    finally:
        if p_close:
            cursor.close()
        return val


def exec_proc(procname:str,  param: [] ,cursor = connection.cursor() ,p_close:bool = False, **kwargs):
    #cursor.callproc("so_test", keywordParameters = dict(p2 = "Y", p3 = "Z"))
    try:
        if kwargs:
            cursor.callproc(procname, keywordParameters=kwargs)
        else:
            cursor.callproc(procname, param)
    except Exception as ex:
        print(ex)
        raise myex.UnhandledError(ex)
    finally:
        if p_close:
            cursor.close()

def exec_sql(sql:str, rettype:str = 'dict' , rows = -1, columnscase:str = 'lower' ,
             cursor = connection.cursor() ,p_close:bool = False , **kwargs):
    val = []
    try:
        cursor.execute(sql)
        if rows == 1:
            val =  cursor.fetchone()
        else:
            if rettype == 'dict':
                val = allrowsto_dict(cursor,columnscase)
            else:
                val =  cursor.fetchall()
    except Exception as ex:
        print(ex)
    finally:
        if p_close:
            cursor.close()
        return val


def select_sqlfunc(funcname :str,
             cursor = connection.cursor(), p_close:bool = False, **kwargs):
    val = None
    try:
        sql = "SELECT " + funcname + " val  from DUAL"
        cursor.execute(sql)
        row = cursor.fetchone()
        val = row[0]
    except:
        pass
    finally:
        if p_close:
            cursor.close()
        return val


def exec_plsqlblock(p_block :str,
             cursor = connection.cursor() ,p_close:bool = False, **kwargs):
    try:
        block = """
        BEGIN  
        {}  
        END;
        """.format(p_block)
        cursor.execute(block)
    except Exception as ex:
        print(ex)
        commonutil.handleerroor(ex)
    finally:
        if p_close:
            cursor.close()


def exec_plsqlblockraw(p_block:str,
             cursor = connection.cursor() ,p_close:bool = False , **kwargs):
    try:
        block = """{}
                """.format(p_block)
        cursor.execute(block)
    except Exception as ex:
        print(ex)
        commonutil.handleerroor(ex)
    finally:
        if p_close:
            cursor.close()

def get_lookupattribute(lookuptype:str, lookupcode:str, attr:int = 1, defval = None,
             cursor = connection.cursor() ,p_close:bool = False  ):
    retval = None
    try:
        retval = cursor.callfunc('Cmn_Common_Pkg.Get_LookupAttributeValues'
                                , str , [lookuptype,lookupcode,attr])
        if retval is None:
            retval = defval
    except:
        pass
    finally:
        if p_close:
            cursor.close()
        return retval


def get_itemprice(price:int, suid:int, itemid:int = None,
             cursor = connection.cursor() ,p_close:bool = False ):
    try:
        priceincvat  = exec_int_func('price_pkg.get_susp',[itemid,suid,price, 'VAT'],cursor=cursor, p_close=False)
        priceexlvat   = exec_int_func('price_pkg.get_susp',[itemid,suid,price,'NOVAT'],cursor=cursor, p_close=False)
    except:
        pass
    finally:
        if p_close:
            cursor.close()
        return priceincvat, priceexlvat


def get_sublocation_id(locationid, sublocation,
             cursor = connection.cursor() ,p_close:bool = False ):
    return select_sqlfunc("Mobile_Pkg.get_SubLocationId({0},upper('{1}'))".format(locationid, sublocation),
                          cursor=cursor,p_close=p_close)

def get_default_sublocationid(locationid, itemid, locgroup:str ='PRIMARY SALES',
             cursor = connection.cursor() ,p_close:bool = False ):
    return select_sqlfunc("Location_Pkg.Get_ItemDefSubLocByGroup({0},{1},{2})".format(
                     locationid, itemid,locgroup), cursor=cursor, p_close=p_close)

def get_externallocation(cursor = connection.cursor() ,p_close:bool = False ):
    return  select_sqlfunc("cmn_common_Pkg.Get_DefaultLookupCode('ITEM_EXTERNAL_LOCATIONS')",cursor=cursor, p_close=p_close)

def get_primarysubloc(subloctype:str = 'PRIMARY SALES', locationid:int = 1,
             cursor = connection.cursor() ,p_close:bool = False ):
    return select_sqlfunc("Location_Pkg.Get_PrimarySubLoc('{0}',{1})".format('PRIMARY GRN',
                                               locationid),cursor=cursor, p_close=p_close)

def get_username(userid):
    if commonutil.hasintvalue(userid):
        username = generic.CRUDApi(db.db_engine,CmnUsers,p_rettype='getuk',p_pk='user_id',
                               p_unique='user_name').get_first(p_rettype='getuk',p_filterby={'user_id':userid})
        if commonutil.hasstrvalue(username):
            return username
    return "unknown"

def is_db_object_exists(p_objectname,cursor = connection.cursor() ,p_close:bool = False ):
    val = 0
    retval = exec_sql("Select nvl(count(1),0) val from user_objects where object_name = '{}'".format(p_objectname),
                      columnscase='lower', cursor=cursor, p_close=False)
    if len(retval) > 0:
        val = retval[0]['val']
    return val

def is_constraint_exists(p_objectname):
    val = 0
    retval = exec_sql("Select nvl(count(1),0) val from user_constraints where constraint_name = '{}'".format(p_objectname), columnscase='lower')
    if len(retval) > 0:
        val = retval[0]['val']
    return val

def get_col_def(p_tablename:str, p_columnname:str):
    sql = """select tname object_name,  cname column_name, coltype data_type,
                nvl(To_Char(Decode(coltype,'NUMBER',Precision,width)),'10') data_width,
                nvl(To_Char(Decode(coltype,'NUMBER',Scale,Precision)),'0') data_precision,
                defaultval  , decode(nulls,'NULL','True','False') nullable 
              from col
              Where tname = '{}'
              and   cname = '{}'
                """.format(p_tablename.upper(),p_columnname.upper())
    retval = exec_sql(sql, columnscase='lower')
    defkey = 'defaultval'
    if len(retval) > 0:
        retval = retval[0]
        defaultval = retval[defkey]
        if not commonutil.hasstrvalue(defaultval):
            retval[defkey] = 'None'
        try:
            if 'NEXTVAL' in defaultval:
                defaultval = '.'.join(defaultval.split('.')[1:])
                retval[defkey] = defaultval
        except:
            pass
        finally:
            return retval
    return {}