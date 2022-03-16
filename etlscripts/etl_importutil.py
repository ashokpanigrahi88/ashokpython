from datetime import datetime
from sqlalchemy import DateTime, Date
from os import (environ, path)
import numpy as np
import pandas as pd
from sqlalchemy.orm import  scoped_session, mapper, sessionmaker
from oratechetl import (commonutil, utilconfig)
from oratechetl.model import (InvItemCategories, InvItemSubCategories,InvManufacturers,
                              ApSupplierProfiles, ApSuppliers, ArCustomerProfiles, ArCustomers,
                              CmnTaxCodes,CmnPaymentMethods, CmnPaymentTerms,CmnUnitOfMeasurements,
                              InvItemMasters,InvItemSalesUnits,InvItemBarcodes,InvPriceTypes,
                              InvItemPrices, InvLocations, TpStockLines)
from oratechetl import imp_exp_settings as impexp
from crudapi import generic as crud
import oratechetl.db as db
from oratechetl import set_session as session
import logging
"""
df['Event'] = np.where((df.Event == 'Painting'),'Art',df.Event)
df.loc[(df.Event == 'Dance'),'Event']='Hip-Hop'
"""
def read_sourcefile(p_importsource, p_file, p_rettype = 'dict'):
    sourcedir = utilconfig.get_directory(p_importsource,p_basedir='importbase')
    sourcefile = "{}{}".format(sourcedir,p_file)
    if '.csv' in p_file:
        df = pd.read_csv(sourcefile)
    else:
        df = pd.read_json(sourcefile,orient=utilconfig.DEFAULT_JSON_ORIENT)
    df = df.drop(utilconfig.get_ignoredcolumns(), axis=1, errors='ignore')
    df = df.replace({np.NAN: None})
    if p_rettype == 'dict':
        df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    return df


def df_loaddata(p_loadsurce, p_sql:str = "select 1 from dual", p_rettype = 'default'):
    conn = utilconfig.get_connection(p_loadsurce)
    df = pd.DataFrame()
    df = pd.read_sql(p_sql, con=conn)
    df.columns = map(str.lower, df.columns)
    df.fillna("",inplace=True)
    df = df.replace({np.NAN: None})
    return df


def import_singletable(p_importsource,
                       p_targetdb,
                       p_file,
                       p_tableclass,
                       p_pk,
                       p_unk,
                       p_compositepk:{} = {},
                       p_df = None):
    db_conn = utilconfig.get_connection(p_targetdb)
    Session = sessionmaker(bind=db.db_engine)
    session = Session()
    df = p_df
    try:
        if p_df:
            df = p_df
        else:
            df = read_sourcefile(p_importsource,p_file)
        tableclass = p_tableclass
        table = tableclass.__tablename__
        pk = p_pk
        unk = p_unk
        compositepk = p_compositepk
        id = None
        for row in df:
            try:
                id = crud.get_idbyuk(db_conn,table,row[unk],p_retfield='pk')
                if commonutil.hasstrvalue(id):
                    crud.CRUDApi(db.db_engine,tableclass, p_crudtype='import',p_compositepk=compositepk,p_session=session,
                                 p_data=row,p_pk=pk,p_unique=unk).merge()
                else:
                    crud.CRUDApi(db.db_engine,tableclass,p_data=row, p_crudtype='import',p_compositepk=compositepk,p_session=session,
                                 p_pk=p_pk,p_unique=unk).insert()
            except Exception as ex:
                logging.error(ex)
                #session.close()
        session.close()
    except Exception as ex:
        print(ex)
    return df

def import_category(p_importsource, p_targetdb,p_file='categories.json'):
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,
                       p_tableclass=InvItemCategories,p_pk='category_id',p_unk='category_name')


def import_sub_category(p_importsource, p_targetdb,p_file='sub_categories.json'):
    db_conn = utilconfig.get_connection(p_targetdb)
    df = read_sourcefile(p_importsource,p_file,p_rettype='default')
    tableclass = InvItemSubCategories
    table = tableclass.__tablename__
    pk = 'sub_category_id'
    unk = 'sub_category_name'
    parentpk = 'iic_category_id'
    parentunk = 'category_name'
    compositepk = {}
    for i, row in df.iterrows():
        parentval = df.at[i,parentunk]
        categoryid =  crud.get_idbyuk(db_conn,'inv_item_categories',parentval,p_retfield='pk')
        df.at[i,parentpk] = categoryid
    df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    db_conn = utilconfig.get_connection(p_targetdb)
    for row in df:
        categoryid = row[parentpk]
        filterby = {parentpk: categoryid, unk: row[unk]}
        compositepk['where'] = "{} = {} and {} = '{}'".format(parentpk, categoryid, unk, row[unk])
        if commonutil.hasstrvalue(row[unk]):
            id = crud.get_idbyuk(db_conn,table,p_value=None,p_retfield='pk',p_filter=filterby)
            try:
                if commonutil.hasstrvalue(id):
                    crud.CRUDApi(db.db_engine,InvItemSubCategories,p_data=row, p_crudtype='import',
                                 p_compositepk=compositepk,
                                 p_pk=pk,p_unique=unk).merge()
                else:
                    crud.CRUDApi(db.db_engine,InvItemSubCategories,p_data=row, p_crudtype='import',
                                 p_compositepk=compositepk,
                                 p_pk=pk,p_unique=unk).insert()
            except Exception as ex:
                logging.error(ex)
                raise

def import_manufacturer(p_importsource, p_targetdb,p_file='manufacturers.json'):
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,
                       p_tableclass=InvManufacturers,p_pk='manf_id',p_unk='manf_name')


def import_supplierprofile(p_importsource, p_targetdb,p_file='supplier_profiles.json'):
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,
                       p_tableclass=ApSupplierProfiles,p_pk='sup_profile_id',p_unk='sup_profile_name')


def import_paymentterms(p_importsource, p_targetdb,p_file='payment_terms.json'):
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,
                       p_tableclass=CmnPaymentTerms,p_pk='cpt_id',p_unk='terms_days')

def import_locations(p_importsource, p_targetdb,p_file='locations.json'):
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,
                       p_tableclass=InvLocations,p_pk='location_id',p_unk='location_name')

def import_customerprofile(p_importsource, p_targetdb,p_file='customer_profiles.json'):
    db_conn = utilconfig.get_connection(p_targetdb)
    df = read_sourcefile(p_importsource,p_file,p_rettype='default')
    for i, row in df.iterrows():
        fk = 'cpt_cpt_id'
        lookup = df.at[i, 'terms_days']
        cptid =  crud.get_idbyuk(db_conn,'cmn_payment_terms',lookup,p_retfield='pk')
        df.at[i, fk] = cptid
    df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,p_df=df,
                       p_tableclass=ArCustomerProfiles,p_pk='cust_profile_id',p_unk='cust_profile_name')

def import_taxcodes(p_importsource, p_targetdb,p_file='tax_codes.json'):
    db_conn = utilconfig.get_connection(p_targetdb)
    df = read_sourcefile(p_importsource,p_file,p_rettype='default')
    for i, row in df.iterrows():
        fk = 'gac_gl_account_id'
        lookup = df.at[i, 'gl_account_code']
        if commonutil.hasstrvalue(lookup):
            lookupid =  crud.get_idbyuk(db_conn,'gl_account_codes',lookup,p_retfield='pk')
            df.at[i, fk] = lookupid
    df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,p_df=df,
                       p_tableclass=CmnTaxCodes,p_pk='tax_code_id',p_unk='tax_code')


def import_suppliers(p_importsource, p_targetdb,p_file='suppliers.json'):
    db_conn = utilconfig.get_connection(p_targetdb)
    df = read_sourcefile(p_importsource,p_file,p_rettype='default')
    for i, row in df.iterrows():
        fk = 'asp_sup_profile_id'
        lookup = df.at[i, 'sup_profile_name']
        if commonutil.hasstrvalue(lookup):
            lookupid =  crud.get_idbyuk(db_conn,'ap_supplier_profiles',lookup,p_retfield='pk')
            df.at[i, fk] = lookupid
        fk = 'ctc_tax_code_id'
        lookup = df.at[i, 'tax_code']
        if commonutil.hasstrvalue(lookup):
            lookupid = crud.get_idbyuk(db_conn, 'cmn_tax_codes', lookup, p_retfield='pk')
            df.at[i, fk] = lookupid
    df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,p_df=df,
                       p_tableclass=ApSuppliers,p_pk='supplier_id',p_unk='supplier_name')


def import_customers(p_importsource, p_targetdb,p_file='customers.json'):
    db_conn = utilconfig.get_connection(p_targetdb)
    df = read_sourcefile(p_importsource,p_file,p_rettype='default')
    for i, row in df.iterrows():
        fk = 'cto_cust_profile_id'
        lookup = df.at[i, 'cust_profile_name']
        if commonutil.hasstrvalue(lookup):
            lookupid =  crud.get_idbyuk(db_conn,'ar_customer_profiles',lookup,p_retfield='pk')
            df.at[i, fk] = lookupid
        fk = 'ctc_tax_code_id'
        lookup = df.at[i, 'tax_code']
        if commonutil.hasstrvalue(lookup):
            lookupid = crud.get_idbyuk(db_conn, 'cmn_tax_codes', lookup, p_retfield='pk')
            df.at[i, fk] = lookupid
        fk = 'cpt_cpt_id'
        lookup = df.at[i, 'terms_days']
        if commonutil.hasstrvalue(lookup):
            lookupid = crud.get_idbyuk(db_conn, 'cmn_payment_terms', lookup, p_retfield='pk')
            df.at[i, fk] = lookupid
    df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,p_df=df,
                       p_tableclass=ArCustomers,p_pk='customer_id',p_unk='customer_name')


def get_lookupid(p_connection, p_lookupkey, p_lookupval , p_lookuptable, p_filter:{} = {}):
    fk = p_lookupkey
    lookup = p_lookupval
    lookuptable = p_lookuptable
    lookupid = None
    if commonutil.hasstrvalue(lookup):
        lookupid = crud.get_idbyuk(p_connection, lookuptable, lookup, p_retfield='pk',p_filter=p_filter)
    if not commonutil.hasintvalue(lookupid):
        return None
    return lookupid

def import_items(p_importsource, p_targetdb,p_file='items.json'):
    db_conn = utilconfig.get_connection(p_targetdb)
    df = read_sourcefile(p_importsource,p_file,p_rettype='default')
    #df = df.iloc[0:500,:]
    for i, row in df.iterrows():
        fk = 'iic_category_id'
        lookup = df.at[i, 'category_name']
        categoryid =  get_lookupid(db_conn,fk,lookup,'inv_item_categories')
        df.at[i, fk] = categoryid
        fk = 'iisc_sub_category_id'
        lookup = df.at[i, 'sub_category_name']
        filterby = {'iic_category_id':categoryid,'sub_category_name':lookup}
        lookupid = get_lookupid(db_conn,fk,lookup,'inv_item_sub_categories',p_filter=filterby)
        if lookupid is None:
            print(i, filterby, row)
            raise
        df.at[i, fk] = lookupid
        fk = 'ctc_tax_code_id'
        lookup = df.at[i, 'tax_code']
        df.at[i, fk] =  get_lookupid(db_conn,fk,lookup,'cmn_tax_codes')
        fk = 'sup_supplier_id'
        lookup = df.at[i, 'supplier_name']
        df.at[i, fk] =  get_lookupid(db_conn,fk,lookup,'ap_suppliers')
        fk = 'im_manf_id'
        lookup = df.at[i, 'manf_name']
        df.at[i, fk] =  get_lookupid(db_conn,fk,lookup,'inv_manufacturers')
    df = df.replace({np.nan: None})
    df = df.replace({np.NAN: None})
    df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,p_df=df,
                       p_tableclass=InvItemMasters,p_pk='item_id',p_unk='item_number')


def import_salesunits(p_importsource, p_targetdb,p_file='item_sales_units.json'):
    is_valid = True
    db_conn = utilconfig.get_connection(p_targetdb)
    df = read_sourcefile(p_importsource,p_file,p_rettype='default')
    #df = df.iloc[0:500,:]
    for i, row in df.iterrows():
        fk = 'iim_item_id'
        lookup = df.at[i, 'item_number']
        try:
            itemid =  get_lookupid(db_conn,fk,lookup,'inv_item_masters')
            if itemid is not None:
                df.at[i, fk] = itemid
            else:
                is_valid = False
                print(i,row)
                raise
        except:
            logging.error('import sales unit falied at {}'.format(i))
            print('validation falied at',i, row)
            raise
        fk = 'uom_id'
        lookup = df.at[i, 'uom_short_desc']
        if lookup != 'None' and commonutil.hasintvalue(lookup):
            df.at[i, fk] =  get_lookupid(db_conn,fk,lookup,'cmn_unit_of_measurements')
    if not is_valid:
        print('validation failed')
        return
    print('validation passed')
    df = df.replace({np.nan: None})
    df = df.replace({np.NAN: None})
    df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,p_df=df,
                       p_tableclass=InvItemSalesUnits,p_pk='su_id',p_unk='su_number')


def import_barcodes(p_importsource, p_targetdb,p_file='item_barcodes.json'):
    is_valid = True
    db_conn = utilconfig.get_connection(p_targetdb)
    df = read_sourcefile(p_importsource,p_file,p_rettype='default')
    for i, row in df.iterrows():
        fk = 'iim_item_id'
        lookup = df.at[i, 'item_number']
        try:
            itemid =  get_lookupid(db_conn,fk,lookup,'inv_item_masters')
            if itemid is not None:
                df.at[i, fk] = itemid
            else:
                is_valid = False
                print('itemid',i,row)
                raise
        except:
            logging.error('import sales unit falied at {}'.format(i))
            print('validation falied at',i, row)
            raise
        fk = 'iisu_su_id'
        lookup = df.at[i, 'su_number']
        try:
            suid = get_lookupid(db_conn, fk, lookup, 'inv_item_sales_units')
            if suid is not None:
                df.at[i, fk] = suid
            else:
                is_valid = False
                print('suid',i, row)
                raise
        except:
            logging.error('import barcodes falied at {}'.format(i))
            print('validation falied at', i, row)
            raise
    if not is_valid:
        print('validation failed')
        return
    print('validation passed')
    df = df.replace({np.nan: None})
    df = df.replace({np.NAN: None})
    df = df.to_dict(orient=utilconfig.DEFAULT_JSON_ORIENT)
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,p_df=df,
                       p_tableclass=InvItemBarcodes,p_pk='barcode_id',p_unk='barcode')


def import_file2table(p_file, p_targettable:str,p_pk,
                    p_db:str='oratech_datahub',
                     p_datasource:str='what_warehouse',
                     p_filedirectory='exportbase'):
    data , v_source = impexp.read_json_data(p_file=p_file, p_filedirectory=p_filedirectory)
    data_this = impexp.load_data_in_memory(p_db=p_db,p_datasource = p_datasource,p_table=p_targettable)
    merge_columns_on = ['third_party_source','third_party_source_ref']
    data[merge_columns_on] = data[merge_columns_on].astype(str)
    data_this[merge_columns_on] = data_this[merge_columns_on].astype(str)
    duplicates = pd.merge(data, data_this, how='inner',
                  on=['third_party_source','third_party_source_ref'])
    data = data.drop(duplicates.index)
    if len(data) == 0:
        print('no new data')
        return
    if len(data) > 0:
        data = impexp.assign_audit_columns(data)
        data.fillna('',inplace=True)
        data = data.replace({np.NaN:None}).replace({np.nan:None})
        columns = list(data.columns)
        table_columns = ','.join(columns)
        value_columns = impexp.formatcolumns(columns)
        v_sql = """MERGE INTO {} t USING DUAL 
                ON ( t.{}  = {} )
                WHEN NOT MATCHED Then 
                INSERT ( {} )
                VALUES ( {})
                """.format(p_targettable,p_pk,':'+p_pk,table_columns,value_columns)
        conn =  utilconfig.get_connection(p_db)
        for i, row in data.iterrows():
            rowvalue = (row[p_pk],*tuple(dict(row).values()))
            with utilconfig.get_connection(p_db) as conn:
                conn.execute(v_sql,conn,rowvalue)

def import_categories(p_db:str='oratech_datahub',p_datasource=None):
    import_file2table(p_db=p_db,
                        p_file ='category',
                        p_filedirectory='exportbase',
                        p_targettable = 'INV_ITEM_CATEGORIES',
                        p_pk = 'category_name',
                        p_datasource=p_datasource)

def import_countries(p_db:str='oratech_datahub',p_datasource=None):
    import_file2table(p_db=p_db,
                        p_file ='countries',
                        p_filedirectory='exportbase',
                        p_targettable = 'CMN_COUNTRIES',
                        p_pk = 'country_code',
                        p_datasource=p_datasource)


def import_stores(p_db:str='oratech_datahub',p_datasource=None):
    import_file2table(p_db=p_db,
                        p_file ='locations',
                        p_filedirectory='exportbase',
                        p_targettable = 'INV_LOCATIONS',
                        p_pk = 'location_name',
                        p_datasource=p_datasource)


def import_thirdpartystock(p_importsource, p_targetdb,p_file='item_locations.json'):
    df = import_singletable(p_importsource=p_importsource,p_targetdb=p_targetdb,p_file=p_file,
                       p_tableclass=TpStockLines,p_pk='tp_stock_line_id',p_unk='tp_uk')

def import_from_epos(p_importsource='what_nuepos', p_targetdb='oratech_datahub',p_file=None):
    import_suppliers(p_importsource,p_targetdb)
    import_manufacturer(p_importsource,p_targetdb)
    import_category(p_importsource,p_targetdb)
    import_sub_category(p_importsource,p_targetdb)
    import_items(p_importsource,p_targetdb)
    import_salesunits(p_importsource,p_targetdb)
    import_barcodes(p_importsource,p_targetdb)
    import_thirdpartystock(p_importsource,p_targetdb)


def import_from_warehouse(p_importsource='what_oratech', p_targetdb='oratech_datahub',p_file=None):
    import_taxcodes(p_importsource,p_targetdb)
    import_paymentterms(p_importsource,p_targetdb)
    import_supplierprofile(p_importsource,p_targetdb)
    import_suppliers(p_importsource,p_targetdb)
    import_manufacturer(p_importsource,p_targetdb)
    import_category(p_importsource,p_targetdb)
    import_sub_category(p_importsource,p_targetdb)
    import_items(p_importsource,p_targetdb)
    import_salesunits(p_importsource,p_targetdb)
    import_barcodes(p_importsource,p_targetdb)
    import_thirdpartystock(p_importsource,p_targetdb)