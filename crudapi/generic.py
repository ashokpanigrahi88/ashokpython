from oratechetl.model import InvItemCategories
from sqlalchemy import and_, or_, text
from sqlalchemy.orm import  scoped_session, mapper, sessionmaker
from oratechetl import (commonutil,dateutil)
from sqlalchemy.ext.declarative import declarative_base
from oratechetl.OratechExceptions import *
from oratechetl.model_helper import (get_classname, get_keybyClass, get_keybyTable)
from oratechetl import OratechExceptions as myex
import logging

Base = declarative_base()

class CRUDApi():
    engine = None
    data = {}
    dml = 'select'
    instance = Base()
    pk = ""
    unique = ""
    columns = '*'
    commitmode = 'auto'
    session = None
    Session = None
    id = None
    unk = None
    selectstatement = None
    compositepk = {}
    crudtype = 'default'
    connection = None
    def __init__(self,p_engine,
            p_instance=Base,
            p_dml:str = 'select',
            p_data:{} = {'id':None},
            p_pk:str = "",
            p_unique:str = "",
            p_columns:str = '*',
            p_commitmode = 'auto',
            p_session = None,
            p_selectstatement = None,
            p_compositepk:{} = {},
            p_crudtype:str = 'default',
            *args,**kwargs):
        """ assigns and validated all parameter """
        self.engine = p_engine
        self.data = p_data
        self.dml = p_dml
        self.instance = p_instance
        self.pk = p_pk
        self.unique = p_unique
        self.columns = p_columns
        self.Session = p_session
        self.get_set_session()
        self.coompositepk = p_compositepk
        self.crudtype = p_crudtype
        if not self.validate():
            pass
        self.id = commonutil.nvl(commonutil.get_key_value(p_data, p_pk), -1)
        self.unk = commonutil.nvl(commonutil.get_key_value(p_data, p_unique), "")
        # remove pk key from data once already assigned or set to none
        self.data.pop(self.pk,None)
        if not p_selectstatement:
            if self.compositepk == {}:
                if 'import' in self.crudtype:
                    self.selectstatement = text("SELECT {} FROM {} WHERE  {} = :unk".format(
                        self.columns, self.instance.__tablename__, self.unique
                    )).params( unk=self.unk)
                else:
                    self.selectstatement = text("SELECT {} FROM {} WHERE {} = :id or {} = :unk".format(
                        self.columns,  self.instance.__tablename__,self.pk, self.unique
                    )).params(id=self.id,unk=self.unk)
            else:
                self.selectstatement = text("SELECT {} FROM {} WHERE {} ".format(
                    self.columns,  self.instance.__tablename__, self.compositepk['where']))
        else:
            self.selectstatement = p_selectstatement

    def __returntype(self, p_row,p_rettype,p_pk, p_unique):
        if p_row:
            if p_rettype == 'getid':
                return getattr(p_row, p_pk)
            if p_rettype == 'getuk':
                return getattr(p_row, p_unique)
            if p_rettype == 'selectdict':
                return p_row.__dict__
        if p_rettype == 'select':
            return p_row

    def get_first(self, p_rettype='selectdict',p_filterby: {} = {}):
        """ returns first row of any table, use this configure tables """
        row = self.session.query(self.instance)
        if p_filterby == {}:
            row = row.first()
        else:
            row = row.filter_by(**p_filterby).first()
        return self.__returntype(row,p_rettype,self.pk, self.unique)

    def get_singlekeyval(self, p_key,p_filterkey = None, p_filterby = None):
        """ returns first row of a table or by given filter """
        qry = self.session.query(self.instance)
        if commonutil.hasstrvalue(p_filterkey):
            row = qry.filter_by(**{p_filterkey:p_filterby}).first()
        else:
            row = self.session.query(self.instance).first()
        if not row:
            return ""
        return row.__dict__[p_key]

    def get_bykey(self,p_key, p_val, p_rettype='getid'):
        """ return id or name by a given field"""
        row = self.session.query(self.instance).filter_by(**{p_key:p_val}).first()
        return self.__returntype(row,p_rettype,self.pk, self.unique)

    def get_set_session(self):
        """ gets or sets new session to the instance"""
        try:
            if not self.Session:
                self.Session = sessionmaker(bind=self.engine)
                self.session = self.Session()
            else:
                self.session = self.Session
        except Exception as ex:
            raise SessionFailed(error=ex)

    def validate(self):
        """ add all initial validation here """
        if not self.engine:
            raise NoEngine
        if not self.session:
            raise SessionFailed
        if self.data == {}:
            raise DataError
        return True


    def shutdown_session(self,exception=None):
        pass

    def get_rows(self,p_where= None):
        """ returns list of rows by given where condition or all rows"""
        try:
            if commonutil.hasstrvalue(p_where):
                stmnt = text("""SELECT {} FROM {} WHERE {}""".format(
                    self.columns, self.instance.__tablename__, p_where)
                )
            rows = self.session.query(self.instance).from_statement(stmnt).all()
            return rows
        except Exception as ex:
            raise myex.SessionFailed(ex)
        finally:
            self.shutdown_session()

    def select(self,p_return=None):
        """ checks data if exist for the supplied data parameter , filters by id or name or number"""
        try:
            rettype = p_return
            if not commonutil.hasstrvalue(rettype):
                rettype = self.dml
            self.row = self.session.query(self.instance).from_statement(self.selectstatement).first()
            return self.__returntype(self.row,rettype,self.pk, self.unique)
        except Exception as ex:
            raise myex.SessionFailed(ex)
        finally:
            self.shutdown_session()

    def insert(self):
        """ inserts if record does not exist"""
        try:
            row = self.select('select')
            if row:
                return row
            newinstance = self.instance()
            commonutil.assignvalues(newinstance, self.data, p_dml='insert')
            setattr(newinstance, self.pk, None)
            if self.commitmode == 'auto':
                self.session.add(newinstance)
                self.session.commit()
            return row
        except Exception as ex:
            print(ex)
            raise InsertFailed(message=ex, data=self.data)
        finally:
            self.shutdown_session()

    def update(self):
        """" Updates an existing row"""
        try:
            self.dml = 'update'
            row = self.select('select')
            updateinstance = self.instance()
            if not row:
                raise NoDataFound(data=self.data)
            commonutil.assignvalues(updateinstance, self.data, p_dml='update')
            setattr(updateinstance,self.pk,row.__dict__[self.pk])
            if self.commitmode == 'auto':
                row = self.session.merge(updateinstance)
                self.session.commit()
            return row
        except Exception as ex:
            raise UpdateFailed(ex,data=self.data)
        finally:
            self.shutdown_session()

    def merge(self):
        """ inserts or updates the data supplied in init parameter"""
        try:
            rowdml = 'update'
            row = self.select('select')
            if not row:
                result = self.insert()
                rowdml = 'insert'
                return result
            result = self.update()
            return result
        except Exception as ex:
            raise
            #raise MergeFailed(data=self.data)
        finally:
            self.shutdown_session()

    def delete(self):
        """ deletes the record if already exists """
        try:
            row = self.select()
            if not row:
                raise NoDataFound(data=self.data)
            if self.commitmode == 'auto':
                row = self.session.delete(row)
                self.session.commit()
                return 1
            return row
        except Exception as ex:
            raise DeleteFailed(message=ex,data=self.data)
        finally:
            self.shutdown_session()

def generateWhere(p_dict:{} = {}):
    if p_dict == {}:
        return '1 = 1'
    try:
        wherestring = "1 = 1 "
        for key, value in p_dict.items():
            if type(value) == str:
                value = "'{}'".format(value)
            wherestring += " and {} = {}".format(key,value)
        return wherestring
    except Exception as ex:
        logging.debug('generateWhere:'+ex)


def get_idbyfilter(p_dbengine = None, p_table = None , p_filterby:{} ={}, p_retfield = 'pk'):
    retfield = p_retfield
    if p_dbengine is None or p_table is None:
        return None
    if p_retfield == 'pk':
        retfield = get_keybyTable(p_table)
    if p_retfield == 'uk':
        retfield = get_keybyTable(p_table,p_retfield)
    if retfield is None:
        retfield = '*'
    wherecaluse = generateWhere(p_dict=p_filterby)
    sql = "SELECT {} FROM {} WHERE {}".format(retfield,p_table,wherecaluse)
    logging.debug('get_idbyfilter:'+sql)
    cur = p_dbengine.cursor()
    result = cur.execute(sql).fetchone()
    if result:
        if retfield == '*':
            return result
        else:
            return result[0]
    return None

def get_tabledata(p_dbengine = None, p_table = None , p_filterby:{} ={}, p_retfield = '*', p_rettype = 'default'):
    retfield = p_retfield
    if p_dbengine is None or p_table is None:
        return None
    if p_retfield == 'pk':
        retfield = get_keybyTable(p_table)
        if retfield is None:
            retfield = '*'
    wherecaluse = generateWhere(p_dict=p_filterby)
    sql = "SELECT {} FROM {} WHERE {}".format(retfield,p_table,wherecaluse)
    logging.debug('get_idbyfilter:'+sql)
    result = p_dbengine.execute(sql).fetchall()
    return result

def get_pkbyThirdPartySource(p_engine, p_table,p_tpsource,p_tpvalue, p_rettype = 'val',  p_retfield='pk'):
    filterby = {'third_party_source':"{}".format(p_tpsource),
                'third_party_source_ref' : "{}".format(p_tpvalue)
                }
    id = get_idbyfilter(p_engine,p_table,filterby)
    if p_rettype == 'exists':
        if commonutil.hasstrvalue(id):
            return True
        else:
            return False
    return id

def get_idbypk(p_engine,p_table,p_value,p_retfield='pk'):
    pk = get_keybyTable(p_table,p_key='pk')
    id = get_idbyfilter(p_engine,p_table,{pk:p_value},p_retfield=p_retfield)
    return id

def get_idbyuk(p_engine,p_table,p_value,p_retfield='uk',p_filter:{} = {} ):
    filterby = p_filter
    if filterby == {}:
        uk = get_keybyTable(p_table,p_key='uk')
        filterby = {uk: p_value}
    id = get_idbyfilter(p_engine,p_table,filterby,p_retfield=p_retfield)
    return id


def get_modelpk(p_model):
    try:
        pk = [col.name for col in p_model.__table__.columns if col.primary_key]
        if len(pk) == 1:
            return pk
        else:
           return ','.join(pk)
    except Exception as ex:
        print('get_modelpk',ex)
        return None

def get_modeluk(p_model):
    try:
        uk = [col.name for col in p_model.__table__.columns if col.unique]
        if len(uk) == 1:
            return uk
        else:
            return ','.join(uk)
    except Exception as ex:
        print('get_modelpk',ex)
        return None

def get_model_columns(p_model):
    try:
        cols = [col.name for col in p_model.__table__.columns]
        return cols
    except Exception as ex:
        print('get_model_columns',ex)
        return None

def get_model_required_columns(p_model):
    try:
        cols = [col.name for col in p_model.__table__.columns if not col.nullable]
        return cols
    except Exception as ex:
        print('get_model_required_columns',ex)
        return None


def get_model_optional_columns(p_model):
    try:
        cols = [col.name for col in p_model.__table__.columns if  col.nullable]
        return cols
    except Exception as ex:
        print('get_model_optional_columns',ex)
        return None

def req_key_exists(p_reqkey:[], p_datakey:[]):
    return all(item in p_datakey for item in p_reqkey)


def missing_keys(p_reqkey:[], p_datakey:[]):
    missing = list(set(p_reqkey).difference(p_datakey))
    if not missing:
        return {}
    return missing


def get_session(p_engine=None, p_session=None):
    """ gets or sets new session to the instance"""
    try:
        session = p_session
        if not session:
            Session = sessionmaker(bind=p_engine)
            session = Session()
        return session
    except Exception as ex:
        raise SessionFailed(error=ex)

def insert(p_tableclass:Base, p_data, p_pk, p_engine=None,p_session=None,p_autonomous=True):
    session = get_session(p_engine=p_engine, p_session=p_session)
    p_data[p_pk] = None
    myinstance = p_tableclass()
    commonutil.assignvalues(myinstance,p_data,p_dml='insert')
    session.add(myinstance)
    if p_autonomous:
        session.commit()

def select(p_tableclass:Base, p_where, p_columns='*', p_engine=None,p_session=None,p_returntype:str='default', **kwargs):
    """ returns list of rows by given where condition or all rows"""
    try:
        session = get_session(p_engine=p_engine, p_session=p_session)
        rows = []
        if commonutil.hasstrvalue(p_where):
            stmnt = text("""SELECT {} FROM {} WHERE {}""".format(
                p_columns, p_tableclass.__tablename__, p_where)
            )
        result = session.query(p_tableclass).from_statement(stmnt).all()
        if not result:
            return -2
        if p_returntype == 'default':
            return result
        if p_returntype == 'dict':
            for row in result:
                rows.append(row.__dict__)
            if len(rows) == 1:
                return rows[0]
        return rows
    except Exception as ex:
        raise myex.SessionFailed(ex)


def update(p_tableclass:Base, p_data, p_pk, p_engine=None,p_session=None,p_autonomous=True):
    session = get_session(p_engine=p_engine, p_session=p_session)
    myinstance = p_tableclass()
    commonutil.assignvalues(myinstance,p_data,p_dml='update')
    session.merge(myinstance)
    if p_autonomous:
        session.commit()

def delete(p_tableclass:Base, p_data, p_pk, p_engine=None,p_session=None,p_autonomous=True):
    session = get_session(p_engine=p_engine, p_session=p_session)
    myinstance = p_tableclass()
    commonutil.assignvalues(myinstance,p_data,p_dml='delete')
    session.delete(myinstance)
    if p_autonomous:
        session.commit()

def dict_to_rawdml(p_table:str, p_pk:str, p_dict:{},p_dml:str='insert into'):
    sql = ""
    values = ""
    columns = ""
    pkval = commonutil.get_key_value(p_dict,p_pk)
    ctr = 0
    if p_dict == {}:
        return sql
    sql = "{} {} ".format(p_dml, p_table)
    for key, value in p_dict.items():
        if 'select' in p_dml:
            columns += ',{}'.format(key)
        elif 'insert' in p_dml:
            if value is not None and key != p_pk:
                columns += ",{}\n".format(key)
                if type(value) == str:
                    values += ",'{}'\n".format(value.replace(",",""))
                elif type(value) == dateutil.datetime:
                    values += ",{}\n".format(dateutil.datetimeto_oracle(value))
                else:
                    values += ",{}\n".format(value)
        elif 'update' in p_dml:
            if value is not None and key != p_pk:
                if type(value) == str:
                    values += ",{} = '{}'\n".format(key ,value)
                elif type(value) == dateutil.datetime:
                    values += ",{} = {} \n".format(key,dateutil.datetimeto_oracle(value))
                else:
                    values += ",{} = {} \n".format(key,value)
        else:
            pass
    if len(columns) > 0 and  columns[0] == ',':
        columns = columns[1:]
    if len(values) > 0 and values[0] == ',':
        values = values[1:]
    print('#columns',len(columns.split(',')))
    print('#values',len(values.split(',')))
    if 'select' in p_dml:
        return "select {} \n From {} \n where {} = {}".format(columns,p_table,p_pk,pkval)
    elif 'update' in p_dml:
        return "update {} \n set  {}  \n where {} = {}".format(p_table,values,p_pk,pkval)
    elif 'insert' in p_dml:
        return "insert into {} ({}) \n VALUES({})  ".format(p_table,columns,values)
    elif 'delete' in p_dml:
        return "delete from {} Where {} = {}".format(p_table,p_pk,pkval)
    else:
        return "invalid dml"


def dict_to_dml(p_table:str, p_pk:str, p_dict:{},p_dml:str='insert into'):
    sql = ""
    values = ""
    columns = ""
    pkval = commonutil.get_key_value(p_dict,p_pk)
    ctr = 0
    if p_dict == {}:
        return sql
    sql = "{} {} ".format(p_dml, p_table)
    for key, value in p_dict.items():
        if 'select' in p_dml:
            columns += ',{}'.format(key)
        elif 'insert' in p_dml:
            #if value is not None and key != p_pk:
            columns += ",{}\n".format(key)
            values += ",:{}\n".format(key)
        elif 'update' in p_dml:
            #if value is not None and key != p_pk:
            values += ",{} = :{}\n".format(key ,key)
        else:
            pass
    if len(columns) > 0 and  columns[0] == ',':
        columns = columns[1:]
    if len(values) > 0 and values[0] == ',':
        values = values[1:]
    print('#columns',len(columns.split(',')))
    print('#values',len(values.split(',')))
    if 'select' in p_dml:
        return "select {} \n From {} where {} = {}".format(columns,p_table,p_pk,pkval)
    elif 'update' in p_dml:
        return "update {} \n set  {}  where {} = {}".format(p_table,values,p_pk,pkval)
    elif 'insert' in p_dml:
        return "insert into {} ({}) \n VALUES({})  ".format(p_table,columns,values)
    elif 'delete' in p_dml:
        return "delete from {} Where {} = {}".format(p_table,p_pk,pkval)
    else:
        return "invalid dml"

def remove_emptykeys(p_dict:{}={}):
    try:
        val = {}
        for key,value in p_dict.items():
            if value is not None:
                val[key] = value
        return val
    except Exception as ex:
        print(ex)
        return p_dict
