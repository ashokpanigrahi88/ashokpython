from sqlalchemy.orm import sessionmaker
from oratechetl import etl_settings
from oratechetl  import db as db
from crudapi import generic as crud
from oratechetl import (utilconfig, commonutil, dbfuncs, model_helper)
from oratechetl.model import (InvItemMasters, InvItemSalesUnits, InvItemBarcodes)
from oratechetl import set_session as sessiondata
from oratechetl import OratechExceptions as myex
import logging


def get_default_val(p_lookup:{} = {},p_lookupcode:str = None, p_default:str ="" ,p_key:str ='attribute1'):
    val = p_default
    if p_lookupcode is None:
        return val
    try:
        val = p_lookup[p_lookupcode][p_key]
        return val
    except Exception as ex:
        print(ex)
        return val


def setitemdefaults(p_itemrow:{}={}, p_default:{} = {},
                        p_hint:str = 'insert', cursor = None):
    vsupcurrencycode = "GBP"
    if not cursor:
        raise myex.UnhandledError('Invalid Cursor, not open')
    if p_hint == 'insert':
        p_itemrow['stock_holding_unit'] = 1
        p_itemrow['case_unit'] = commonutil.key_nvl(p_itemrow,'case_unit', 1)
        try:
            if not commonutil.iskeyempty(p_itemrow,'item_name'):
                p_itemrow['short_desc'] = commonutil.key_nvl(p_itemrow,'short_desc', p_itemrow['item_name'][0:30])
        except:
            p_itemrow['short_desc'] = ""
        p_itemrow['ctc_tax_code_id'] = commonutil.key_nvl(p_itemrow,'ctc_tax_code_id', sessiondata.SESSION_SYS_OPTIONS['tax_code_id'])
        p_itemrow['im_manf_id'] = commonutil.key_nvl(p_itemrow,'im_manf_id', sessiondata.SESSION_INV_OPTIONS['manf_id'])
        p_itemrow['season_code_id'] = commonutil.key_nvl(p_itemrow,'season_code_id', sessiondata.SESSION_INV_OPTIONS['season_code_id'])
        p_itemrow['gac_gl_account_id'] = commonutil.key_nvl(p_itemrow,'gac_gl_account_id',sessiondata.SESSION_INV_OPTIONS['gl_account_id'])
        p_itemrow['sales_gl_account_id'] = commonutil.key_nvl(p_itemrow,'sales_gl_account_id',sessiondata.SESSION_INV_OPTIONS['sales_gl_account_id'])
        p_itemrow['costofsales_gl_account_id'] = commonutil.key_nvl(p_itemrow,'costofsales_gl_account_id',
                                                                sessiondata.SESSION_INV_OPTIONS['costofsales_gl_account_id'])
        p_itemrow['pnl_gl_account_id'] = commonutil.key_nvl(p_itemrow,'pnl_gl_account_id',sessiondata.SESSION_INV_OPTIONS['pnl_gl_account_id'])
        p_itemrow['pricevariance_gl_account_id'] = commonutil.key_nvl(p_itemrow,'pricevariance_gl_account_id',
                                                                  sessiondata.SESSION_INV_OPTIONS['pricevariance_gl_account_id'])
        p_itemrow['balancesheet_gl_account_id'] = commonutil.key_nvl(p_itemrow,'balancesheet_gl_account_id',
                                                                 sessiondata.SESSION_INV_OPTIONS['balancesheet_gl_account_id'])
        p_itemrow['purchaseable'] = commonutil.key_nvl(p_itemrow,'purchaseable',get_default_val(p_default,'purchaseable','Y'))
        p_itemrow['reservable'] = commonutil.key_nvl(p_itemrow,'reservable',get_default_val(p_default,'reservable','Y'))
        p_itemrow['apply_offer'] = commonutil.key_nvl(p_itemrow,'APPly_OFFER',get_default_val(p_default,'apply_offer','Y'))
        p_itemrow['freight'] = commonutil.key_nvl(p_itemrow,'FREIGHT',get_default_val(p_default,'freight','N'))
        p_itemrow['enforce_tax_code'] = commonutil.key_nvl(p_itemrow,'enforce_tax_code',get_default_val(p_default,'enforce_tax_code','N'))
        p_itemrow['serial_numbered'] = commonutil.key_nvl(p_itemrow,'serial_numbered',get_default_val(p_default,'serial_numbered','N'))
        p_itemrow['saleable'] = commonutil.key_nvl(p_itemrow,'saleable',get_default_val(p_default,'saleable','Y'))
        p_itemrow['stockable'] = commonutil.key_nvl(p_itemrow,'stockable',get_default_val(p_default,'stockable','Y'))
        p_itemrow['track_usage'] = commonutil.key_nvl(p_itemrow,'track_usage',get_default_val(p_default,'track_usage','Y'))
        p_itemrow['valuable'] = commonutil.key_nvl(p_itemrow,'valuable',get_default_val(p_default,'valuable','Y'))
        p_itemrow['print_picture'] = commonutil.key_nvl(p_itemrow,'print_picture',get_default_val(p_default,'print_picture','Y'))
        p_itemrow['warrantied'] = commonutil.key_nvl(p_itemrow,'warrantied',get_default_val(p_default,'warrantied','Y'))
        p_itemrow['weighed_item'] = commonutil.key_nvl(p_itemrow,'weighed_item',get_default_val(p_default,'weighed_item','Y'))
        p_itemrow['serviceditem'] = commonutil.key_nvl(p_itemrow,'serviceditem',get_default_val(p_default,'serviceditem','Y'))
        p_itemrow['take_snapshot'] = commonutil.key_nvl(p_itemrow,'take_snapshot',get_default_val(p_default,'take_snapshot','Y'))
        p_itemrow['freight'] = commonutil.key_nvl(p_itemrow,'freight',get_default_val(p_default,'freight','Y'))
        p_itemrow['publish_to_web'] = commonutil.key_nvl(p_itemrow,'publish_to_web',get_default_val(p_default,'publish_to_web','Y'))
        p_itemrow['flaginwebexport'] = commonutil.key_nvl(p_itemrow,'print_picture',get_default_val(p_default,'flaginwebexport','Y'))
        p_itemrow['item_status'] = commonutil.key_nvl(p_itemrow,'item_status',get_default_val(p_default,'item_status','Y'))
        p_itemrow['long_desc'] = commonutil.key_nvl(p_itemrow,'long_desc',p_itemrow['item_name'])
        p_itemrow['sup_supplier_id'] = commonutil.key_nvl(p_itemrow,'sup_supplier_id',sessiondata.SESSION_AP_OPTIONS['supplier_id'])
        p_itemrow['iic_category_id'] = commonutil.key_nvl(p_itemrow,'iic_category_id', sessiondata.SESSION_INV_OPTIONS['category_id'])
        p_itemrow['iisc_sub_category_id'] = commonutil.key_nvl(p_itemrow,'iisc_sub_category_id',
                                                           sessiondata.SESSION_INV_OPTIONS['sub_category_id'])
        p_itemrow['supplier_product_code'] = commonutil.key_nvl(p_itemrow,'supplier_product_code',p_itemrow['item_number'])
        p_itemrow['ipbh_price_break_id'] = commonutil.key_nvl(p_itemrow,'ipbh_price_break_ID',
                                                          sessiondata.SESSION_INV_OPTIONS['price_break_id'])
        p_itemrow['min_qty'] = commonutil.key_nvl(p_itemrow,'min_qty',dbfuncs.exec_int_func("inv_pkg.get_minqty",[p_itemrow['case_unit']],cursor=cursor))
        p_itemrow['max_qty'] = commonutil.key_nvl(p_itemrow,'max_qty',dbfuncs.exec_int_func("inv_pkg.get_maxqty",[p_itemrow['case_unit']],cursor=cursor))
        p_itemrow['reorder_qty'] = commonutil.key_nvl(p_itemrow,'reorder_qty',dbfuncs.exec_int_func("inv_pkg.get_reorderqty",[p_itemrow['case_unit']],cursor=cursor))
        p_itemrow['image_hint'] = commonutil.key_nvl(p_itemrow,'image_hint',get_default_val(p_default,'image_hint','AVAILABLE'))
        if sessiondata.SESSION_INV_OPTIONS['defualt_picture_name'] == 'N':
            p_itemrow['picturetype'] = None
            p_itemrow['picturename'] = None
        else:
            p_itemrow['picturetype'] = commonutil.key_nvl(p_itemrow,'picturetype',sessiondata.SESSION_INV_OPTIONS['picture_type'])
            p_itemrow['picturename'] = commonutil.key_nvl(p_itemrow,'picturename',
                                                  dbfuncs.exec_str_func("INV_PKG.GET_PICTURENAME", [p_itemrow['item_number']],cursor=cursor))

    # end of insert
    if not commonutil.is_keyexist(p_itemrow,'unit_cp'):
        p_itemrow['unit_cp'] = ""
    if not commonutil.is_keyexist(p_itemrow,'case_cp'):
        p_itemrow['case_cp'] = ""
    if commonutil.iskeyempty(p_itemrow,'case_cp')  and not commonutil.iskeyempty( p_itemrow,'unit_cp'):
        p_itemrow['case_cp']  =  p_itemrow['unit_cp'] * p_itemrow['case_unit']
    if commonutil.iskeyempty(p_itemrow,'unit_cp')  and not commonutil.iskeyempty( p_itemrow,'case_cp'):
        p_itemrow['unit_cp']  =  round(p_itemrow['case_cp'] / p_itemrow['case_unit'],2)
    vsupcurrencycode = dbfuncs.exec_str_func('ap_pkg.get_supplierval',[p_itemrow['sup_supplier_id'],'currency_code'],cursor=cursor)
    if commonutil.hasintvalue(p_itemrow['case_cp']):
        p_itemrow['alternate_case_cp'] = dbfuncs.exec_int_func("Price_Pkg.Get_ValueXchanged",[p_itemrow['case_cp'], vsupcurrencycode],cursor=cursor)
        p_itemrow['alternate_unit_cp'] =  dbfuncs.exec_int_func("Price_Pkg.Get_ValueXchanged",[p_itemrow['unit_cp'], vsupcurrencycode],cursor=cursor)
    try:
        p_itemrow['gross_unit_weight'] = commonutil.key_nvl(p_itemrow,'gross_unit_weight', round(p_itemrow['gross_case_weight'] / p_itemrow['case_unit'],3))
        p_itemrow['net_unit_weight'] = commonutil.key_nvl(p_itemrow,'net_unit_weight', round(p_itemrow['net_case_weight'] / p_itemrow['case_unit'],3))
        p_itemrow['case_volume'] = commonutil.key_nvl(p_itemrow,'case_volume',( p_itemrow['case_length']* p_itemrow['case_height'] * p_itemrow['case_width'])/1000)
        p_itemrow['unit_volume'] = commonutil.key_nvl(p_itemrow,'unit_volume', (p_itemrow['unit_length']* p_itemrow['unit_height'] * p_itemrow['unit_width'])/1000)
    except:
        pass
    return p_itemrow

def manage_barcode(cursor,p_barcoderow:{},p_hint:str='APPLY',
                   p_batchid:int = None,
                   p_barcoderep:str ='N',
                   p_dml:str ='merge'):
    barcode = commonutil.get_key_value(p_barcoderow,'barcode')
    itemid = commonutil.get_key_value(p_barcoderow,'iim_item_id')
    itemnumber = commonutil.get_key_value(p_barcoderow,'item_number')
    suid = commonutil.get_key_value(p_barcoderow,'iisu_su_id')
    if p_hint.upper() == 'DELETE':
        cursor.execute(
            "delete inv_item_barcodes where iim_item_id = {} and barcode = '{}'".format(itemid,barcode))
    else:
        dbfuncs.exec_proc('inv02_pkg.add_defaultbarcodes',[itemid,p_batchid,suid,p_hint,barcode,p_barcoderep],cursor=cursor, p_close=False)
        if p_hint.upper() == 'SETPRIMARY':
            cursor.execute(
                "UPDATE inv_item_barcodes set primary_flag = 'N' where iim_item_id = {}".format(itemid)
                    )
            cursor.execute("UPDATE inv_item_barcodes set primary_flag = 'y' where iim_item_id = {} and barcode = '{}'".format(itemid,barcode))

class ItemAPI:
    itemclass = InvItemMasters
    itemtable = itemclass.__tablename__
    suclass = InvItemSalesUnits
    sutable = suclass.__tablename__
    barcodeclass = InvItemBarcodes
    barcodetable = barcodeclass.__tablename__
    itempk = 'item_id'
    itemuk = 'item_number'
    supk = 'su_id'
    suuk = 'su_number'
    barcodepk = 'barcode_id'
    barcodeuk = 'barcode'
    engine = db.db_engine
    Session = sessionmaker()
    connection = None
    cursor = None
    itemrow = {}
    itemkeys = []
    surow = [{}]
    barcoderow = [{}]
    item_req = crud.get_model_required_columns(itemclass)
    su_req = crud.get_model_required_columns(suclass)
    barcode_req  = crud.get_model_required_columns(barcodeclass)
    itemdefaults = {}
    dmltype = 'merge'
    def __init__(self,p_itemrow:{}={}, p_surow:[{}] = [{}], p_barcoderow:[{}]=[{}],p_dmltype:str = 'merge',
                 p_engine = db.db_engine, p_session = None):
        self.itemrow = p_itemrow
        self.surow = p_surow
        self.barcoderow = p_barcoderow
        self.engine = p_engine
        self.Session = p_session
        self.get_set_session()
        self.dmltype = p_dmltype
        self.itemkeys = self.get_keys(self.itemrow)
        self.connection = db.db_raw_connection

    def get_set_session(self):
        """ gets or sets new session to the instance"""
        try:
            if not self.Session:
                self.Session = sessionmaker(bind=self.engine)
                self.session = self.Session()
            else:
                self.session = self.Session()
        except Exception as ex:
            raise myex.SessionFailed(error=ex)

    def get_keys(self,p_dict:{}):
        try:
            return p_dict.keys()
        except:
            return []

    def validate_item(self,p_hint='validate'):
        try:
            if not crud.req_key_exists(self.itemkeys, self.item_req):
                raise myex.ValidationError('required keys missing',self.item_req)
            missing = crud.missing_keys(self.item_req,self.itemkeys)
            if len(missing) > 0:
                raise myex.ValidationError('missing required columns {}',format(missing))
            return True
        except Exception as ex:
            return False

    def validate_su(self,p_su:{} = {}, p_hint='validate'):
        try:
            if not p_su:
                return True
            sukeys = p_su.keys()
            if not crud.req_key_exists(sukeys, self.su_req):
                raise myex.ValidationError('required keys missing',self.su_req)
            missing = crud.missing_keys(self.su_req,sukeys)
            if len(missing) > 0:
                raise myex.ValidationError('missing required columns {}',format(missing))
            return True
        except Exception as ex:
            return False

    def validate_barcode(self,p_barcode:{} = {}, p_hint='validate'):
        try:
            if not p_barcode:
                return True
            barcodekeys = p_barcode.keys()
            if not crud.req_key_exists(barcodekeys, self.barcode_req):
                raise myex.ValidationError('required keys missing',self.barcode_req)
            missing = crud.missing_keys(self.barcode_req,barcodekeys)
            if len(missing) > 0:
                raise myex.ValidationError('missing required columns {}',format(missing))
            return True
        except Exception as ex:
            return False

    def set_connection(self, p_db = None):
        if p_db is None or not p_db:
            self.connection = utilconfig.get_raw_connection(p_db)

    def get_cursor(self):
        if not self.cursor:
            self.cursor = self.connection.cursor()
        return self.cursor

    def get_colval(self,p_val, p_return:str = 'item_id',
                   p_table='inv_item_masters',p_by='item_number',
                   p_filter = None, p_sql = None, p_rettype = 'scalar'):
        if p_sql is not None:
            sql = p_sql
        elif p_filter is not None:
            sql = "select {}  from {} WHERE {}  ".format(p_return,p_table,p_filter)
        else:
            sql = "select {}  from {} WHERE {} = '{}'  ".format(p_return,p_table,p_by,p_val)
        retval = None
        retvals = []
        print(sql)
        try:
            with self.engine.connect() as conn:
                results =  conn.execute(sql)
                for row in results:
                    if p_rettype == 'scalar':
                        retval = row[0]
                    else:
                        retval = dict(zip(row.keys(), row.values()))
                    if p_rettype == 'many':
                        retvals.append(retval)
                    else:
                        retvals = retval
                        break
        except Exception as ex:
            print(ex)
            retvals = None
            logging.error(ex)
        finally:
            if retvals == []:
                return None
            return retvals

    def get_item_id(self,p_val,p_by='item_number'):
        return commonutil.nvl(self.get_colval(p_val = p_val,p_by=p_by),-2)

    def get_item_number(self, p_val,p_by='item_id'):
        return self.get_colval(p_val=p_val,p_return='item_number',p_by=p_by)

    def get_item_row(self, p_val,p_rettype:str='row',p_by='item_number'):
        if p_rettype=='empty' or p_rettype=='default':
            row = model_helper.get_row_type(self.itemclass)
            if p_rettype=='default':
                row = setitemdefaults(row)
        else:
            row = self.get_colval(p_val=p_val,p_rettype='row',p_return='*', p_by=p_by)
        return row


    def get_su_id(self,p_val,p_by = 'su_number'):
        return commonutil.nvl(self.get_colval(p_val=p_val,p_by=p_by,p_return='su_id',p_table='inv_item_sales_units'),-2)

    def get_su_number(self, p_val,p_by='su_id'):
        return self.get_colval(p_val=p_val, p_by=p_by, p_return='su_number', p_table=self.sutable)

    def get_su_row(self, p_val,p_rettype:str='row',p_by='su_number'):
        if p_rettype=='empty':
            row = model_helper.get_row_type(self.suclass)
        else:
            row = self.get_colval(p_val=p_val,p_rettype='row',p_return='*',p_by=p_by,p_table=self.sutable)
        return row

    def barcode_exists(self, p_val,p_by='barcode'):
        try:
            val = self.get_colval(p_val=p_val, p_by=p_by, p_return='barcode', p_table=self.barcodetable)
            if val == p_val:
                return True
        except:
            return False

    def get_barcode(self, p_val,p_by='item',p_primary=True):
        if p_by == 'item':
            fil_ter = "iim_item_id = {}  ".format(p_val)
        else:
            fil_ter = "iisu_su_id = {}  ".format(p_val)
        if p_primary:
            fil_ter +=  " and primary_flag = 'Y' "
        return self.get_colval(p_val=p_val, p_filter=fil_ter, p_return='barcode', p_table=self.barcodetable)

    def get_barcode_row(self, p_val = None,p_rettype:str='row',p_by='barcode'):
        if p_rettype=='empty':
            row = model_helper.get_row_type(self.barcodeclass)
        else:
             row = self.get_colval(p_val=p_val,p_rettype='row',p_return='*',p_by=p_by,p_table=self.barcodetable)
        return row

    def get_su_bysalesunit(self, p_itemid, p_salesunit:int = 1):
        fil_ter = "iim_item_id = {} and sales_unit = {}".format(p_itemid,p_salesunit)
        row = self.get_colval(p_val=None,p_filter=fil_ter,p_rettype='row',p_return='*',p_table=self.sutable)
        return row

    def get_su_byitem(self, p_itemid):
        fil_ter = "iim_item_id = {} ".format(p_itemid)
        row = self.get_colval(p_val=None,p_filter=fil_ter,p_rettype='many',p_return='*',p_table=self.sutable)
        return row

    def get_barcode_byitem(self, p_itemid, p_suid = None):
        fil_ter = "iim_item_id = {} ".format(p_itemid)
        if commonutil.hasintvalue(p_suid):
            fil_ter += " iisu_su_id = {}".format(p_suid)
        row = self.get_colval(p_val=None, p_filter=fil_ter, p_rettype='many', p_return='*', p_table=self.barcodetable)
        return row

    def set_item_defautls(self,p_itemdefault:{} = {}):
        self.itemdefaults = p_itemdefault

    def get_system_defautls(self,p_itemdefault:str = 'ITEM_DEFAULTS'):
        try:
            result = {}
            with self.engine.connect() as connection:
                results = connection.execute(""" Select lookup_code,lookup_meaning,description,
                                        attribute1,attribute2,attribute3,attribute4
                                        From cmn_lookup_codes Where clt_lookup_type ='{}' """.format(p_itemdefault))
                for row in results:
                    result[row.lookup_code.lower()] = dict(zip(row.keys(), row.values()))
            self.itemdefaults = result
        except Exception as ex:
            logging.error('item defaults-{}'.format(ex))
            self.itemdefaults = {}

    def get_default_val(self,p_code, p_attr='attribute1',p_default:str =""):
        val = p_default
        try:
            val = self.itemdefaults[p_code][p_attr]
        except:
            pass
        finally:
            return val

    def assign_defaults(self, p_hint:str = 'insert'):
        cursor = self.get_cursor()
        self.itemrow = setitemdefaults(self.itemrow,cursor=cursor)

    def __errorifnotexist(self,p_val:int):
        val = commonutil.nvl(p_val,-2)
        if val <= 0:
            raise ValueError('invalid ID / Number')

    def __errorifnotexist(self, p_val:str):
        val = commonutil.nvl(p_val,'-NONE-')
        if val == '-NONE-':
            raise ValueError('invalid ID / Number')

    def add_sales_unit(self, p_itemid:int, p_salesunit:int = 1, p_itemnumber = None):
        suid = -1
        try:
            if not commonutil.hasintvalue(p_itemid):
                p_itemid = self.get_item_id(p_itemnumber)
            self.__errorifnotexist(p_itemid)
            cursor = self.get_cursor()
            dbfuncs.exec_proc("Price_Pkg.CreateSalesUnit",param=[p_salesunit,p_itemid],cursor=cursor,p_close=False)
            suid = dbfuncs.exec_int_func("inv_pkg.getsuidbyitemid",param=[p_itemid,None,p_salesunit],cursor=cursor, p_close=False)
            surow = self.get_su_row(p_val=suid,p_by=suid)
        except Exception as ex:
            raise myex.UnhandledError(ex)
        finally:
            cursor.close()
            self.connection.commit()
            return suid

    def delete_sales_unit(self, p_itemid:int, p_salesunit:int = 1, p_itemnumber = None):
        suid = -1
        try:
            if not commonutil.hasintvalue(p_itemid):
                p_itemid = self.get_item_id(p_itemnumber)
            self.__errorifnotexist(p_itemid)
            if p_salesunit == 1:
                return 'Cannont delete'
            sql = 'Delete {} Where iim_item_id = {} and sales_unit = {} '.format(self.sutable,p_itemid,p_salesunit)
            print(sql)
            cursor = self.get_cursor()
            cursor.execute(sql)
        except Exception as ex:
            print(ex)
            raise myex.UnhandledError(ex)
        finally:
            cursor.close()
            self.connection.commit()
            return 'deleted'

    def apply_price_template(self, p_itemid:int, p_templatecode:str, p_itemnumber = None):
        suid = -1
        try:
            if not commonutil.hasintvalue(p_itemid):
                p_itemid = self.get_item_id(p_itemnumber)
            self.__errorifnotexist(p_itemid)
            cursor = self.get_cursor()
            dbfuncs.exec_proc("inv02_pkg.apply_PriceTemplate",param=[p_templatecode,None,p_itemid],cursor=cursor,p_close=False)
            suid = dbfuncs.exec_int_func("inv_pkg.getsuidbyitemid",param=[p_itemid,None,1],cursor=cursor, p_close=False)
        except Exception as ex:
            raise myex.UnhandledError(ex)
        finally:
            cursor.close()
            self.connection.commit()
            return suid

    def manage_barcode(self,p_barcode = None,p_itemid = None, p_suid = None,p_hint='APPLY',**kwargs):
        try:
            barrow = {'iim_item_id': p_itemid, 'iisu_su_id': p_suid, 'barcode': p_barcode}
            cursor = self.get_cursor()
            print(cursor)
            if not kwargs:
                barrow.update(kwargs)
            manage_barcode(cursor=cursor,p_barcoderow=barrow, p_hint=p_hint.upper())
        except Exception as ex:
            print(ex)
        finally:
            cursor.close()
            self.connection.commit()

    def manage_item(self,p_hint:str='insert'):
        try:
            dmlstatus = 'unknown'
            itemrow = self.itemrow.copy()
            itemnumber = commonutil.get_key_value(itemrow,self.itemuk)
            itemid = commonutil.get_key_value(itemrow,self.itempk)
            self.get_set_session()
            iteminstance = crud.CRUDApi(self.engine,self.itemclass, p_crudtype='import',p_compositepk={},
                                        p_session=self.session,
                             p_data=itemrow,p_pk=self.itempk,p_unique=self.itemuk)
            if 'insert' in p_hint:
                iteminstance.insert()
                dmlstatus = 'inserted'
            if 'update' in p_hint and commonutil.isvalidid(itemid):
                iteminstance.update()
                dmlstatus = 'updated'
            if p_hint == 'delete' and commonutil.isvalidid(itemid):
                iteminstance.delete()
                dmlstatus = 'deleted'
            return dmlstatus
        except Exception as ex:
            return 'error: please check log files:{}'.format(ex)