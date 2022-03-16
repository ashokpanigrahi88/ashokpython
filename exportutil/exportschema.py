import pandas as pd
import dbconfig as cn_config
WEB_EXPORT = {
    'category':("inv_item_categories",
                """  category_id,Category_Name,Category_code,key_words,Last_Update_Date,Delete_Flag """,
                '1 = 1',' 1 ','category.json',''),
    'sub_category':("inv_item_sub_categories",
                """ Sub_Category_ID,IIC_category_id Category_ID,
                    Sub_Category_Name,Sub_Category_code,key_words,Last_Update_Date,Delete_Flag """,
                '1 = 1','1','sub_category.json',''),
    'tax_code':("cmn_tax_codes",
                """ tax_code_id,tax_code,tax_rate,tax_desc,Last_Update_Date,Delete_Flag """,
                '1 = 1','1','tax_codes.json',''),
    'season':("cmn_seasons_V",
                """ SEASON_CODE_ID,SEASON_CODE,SEASON_DESC,BUYING_PERIOD_FROM,BUYING_PERIOD_TO,
                BU_ID,SEASON_COMMENT,
                SELLING_PERIOD_FROM,SELLING_PERIOD_TO,LAST_UPDATE_DATE,Delete_Flag """,
                ' 1 = 1 ','1','seasons.json',''),
    'customer':("ar_customers_v",
            """   CUSTOMER_ID,CUSTOMER_NUMBER,CUST_TITLE,
        CUSTOMER_NAME,ACCOUNT_ALLOWED,ATTRIBUTE1,ATTRIBUTE2,BALANCE,BILLTO_ADDRESS_LINE1,
        BILLTO_CITY,BILLTO_COUNTRY_CODE,BILLTO_COUNTY,BILLTO_POST_CODE,BU_ID,CONSOLIDATE_ITEMS,CONTACT_FORENAME,
        CONTACT_FULL_NAME,CONTACT_SURNAME,CPT_CPT_ID,CREATED_BY,CREATION_DATE,CTC_TAX_CODE_ID Tax_Code_ID,CTP_CUST_PROFILE_ID Cust_Profile_Id,
        CURRENCY_CODE,CUSTOMER_CATEGORY,CUSTOMER_CLASS_CODE,CUSTOMER_HOLD,CUSTOMER_MARKUPDOWN,CUSTOMER_PRICENAME,CUST_CREDIT_LIMIT,CUST_PASSWORD,
        CUST_VATREGNO,EMAIL,FAX,FREIGHT_HEADER_ID,FREIGHT_LINE_ID,FTP_CONTACT,FTP_PASSWORD,
        FTP_PORT,FTP_SERVER,FTP_SERVICE_PROVIDER,FTP_USER_NAME,GL_ACCOUNT_ID,HOLD_REASON,HOST_IMAGE_PATH1,
        HOST_IMAGE_PATH2,INVOICED_AMOUNT,IPT_PRICE_TYPE_ID,ITEM_POP_METHOD,
        LOCATION_ID,LOGIN_NAME,MAX_VALUE,MIN_DEPOSIT_AMOUNT,MIN_ITEM_SU_TYPE,MIN_ITEM_SU_VALUE,MIN_VALUE,MOBILE,
        ORIG_SYSTEM_REF,ORIG_SYSTEM_REF_HDR,PAID_AMOUNT,PHONE1,PHONE2,PICTURENAME,PICTURETYPE,PMNT_METHOD_ID,
        PRIMARY_CUSTOMER_ID,PRINT_CUSTOMER_NAME,RESERVE_ITEM,SHIPTO_ADDRESS_LINE1,
        SHIPTO_CITY,SHIPTO_COUNTRY_CODE,SHIPTO_COUNTY,SHIPTO_POST_CODE,TAKE_DEPOSIT,
        UPDATE_SOURCE,UPLOAD_INSTOCK_ITEMS,UPLOAD_ITEMS,WWW,WWW_CUSTOMER_CATEGORY,WWW_END_DATE,WWW_MARKUPDOWN,
        WWW_MIN_ORDER_FREESHIP,WWW_MIN_ORDER_VALUE,WWW_PRICE_BREAK_DISPLAY,WWW_PRICE_TYPE_ID,
        WWW_START_DATE,WWW_SUBSCRIPTION_PREFERENCE,
        AR_PAYMENT_PKG.Get_PaymentTerms(cpt_Cpt_Id) PAYMENT_TERM,
        SHIPTO_ADDRESS_TYPE,Last_Update_Date,Delete_Flag """, '1 = 1', ' 1 ' ,'customers.json',''),
    'manufacturer':("inv_manufacturers_v",
                """ MANF_ID,MANF_NAME,MANF_NUMBER,MANF_SHORT_NAME,
                ADDRESS_LINE1,ATTRIBUTE1,ATTRIBUTE2,BU_ID,CITY,CONTACT_NAME,
                COUNTRY_CODE,COUNTY,EMAIL,
                FAX,MOBILE,PHONE1,PHONE2,POST_CODE,WWW,Last_Update_Date,Delete_Flag """,
                '1 = 1','1','manufacturers.json',''),
    'cust_fixed_price':("AR_CUSTOMERFIXEDPRICE_V a",
                """ a.CUSTOMER_ID,a.CUSTOMER_NAME,a.CUSTOMER_NUMBER,a.ACTIVE,a.BU_ID,
                a.START_DATE_ACTIVE,a.END_DATE_ACTIVE
                ,a.ITEM_ID,a.ITEM_NAME,a.ITEM_NUMBER,a.MIN_QTY,a.MIN_QTY_SOURCE,a.OVERHEAD_PRICE
                ,a.PRICE,a.PRICE_LIST_ID,a.PRICE_TYPE,a.PRICE_TYPE_ID,
                a.PRICE_TYPE_NAME,a.Last_Update_Date,a.Delete_Flag """,
                ' EXISTS   (select NULL from  inv_itemsCantoWWW_v x Where x.Item_Id = a.Item_ID)  ',
                        ' a.Customer_Id,a.Item_ID','cust_fixed_prices.json',''),
    'cust_balance':("REP_CUSTOMERBALANCE_V",
                """ * """,
                ' 1 = 1 ','1','cust_balances.json',''),
    'item':("inv_item_masters_v",
            """ Item_Id,Item_Number,Item_Name,Item_Status,IPBH_PRICE_BREAK_ID Price_Break_ID, 
            Item_Comment,Item_Specifications, Customer_Notes1,Customer_Notes2,Customer_Notes3,
            Gross_Unit_Weight,CTC_Tax_Code_ID Tax_Code_Id,IISC_Sub_Category_ID Sub_Category_ID,
            IIC_Category_ID Category_Id,Net_Unit_Weight,Stockable,Saleable,Purchaseable,
            Unit_Volume,Unit_height,Unit_width,Unit_Length,Last_Update_Date,Supplier_Product_Code,
            Short_Desc,Long_Desc,Case_Unit,Start_Date_Active,End_Date_Active, Season_Code_Id,
            Similar_Item_concated,Enforce_Tax_Code,Apply_Offer,publish_to_web,IM_MANF_ID MANF_ID,
            picturetype,item_number||'.'||lower(nvl(picturetype,'jpg')) picturename,picturename1,picturename2,picturename3, 
            technical_specs,technical_specs_file """,
                " publish_to_web = 'Y' " ,' 1 ' ,'items.json',''),
    'item_hint':("INV_ITEMWEBHINTS_V",
                """ ITEM_ID,BATCH_ID,BATCH_LINE_ID,SL_NO,NAME,BATCH_NAME,ACCESS_LEVEL,ACTIVE,ATTRIBUTE1,
                ATTRIBUTE2,ATTRIBUTE3,ATTRIBUTE4,BARCODE,BU_ID,
                DATE_FROM,DATE_TO,DESCRIPTION,HEADERDATEFROM,HEADERDATETO,ITEM_BATCH_CATEGORY,
                SU_ID,LAST_UPDATE_DATE,Delete_Flag """,
                ' 1 = 1 ','1','item_hints.json',''),
    'item_info':(" cmn_Additional_Info_V ",
                """ INFO_SOURCE_ID ITEM_ID,INFO_ID,INFO_POSITION,INFO_SOURCE,INFO_TYPE_CODE,SL_NO,
                ACTIVE,BU_ID,DATE_ACTIVE_FROM,DATE_ACTIVE_TO,INFO_ATTRIBUTE1,
                INFO_ATTRIBUTE2,INFO_ATTRIBUTE3,INFO_ATTRIBUTE4,
                INFO_ATTRIBUTE5,INFO_ATTRIBUTE6,INFO_GROUP_CODE,LAST_UPDATE_DATE,Delete_Flag """,
                " Info_Source = 'INV_ITEM_MASTERS' " ,'1','item_info.json',''),
    'item_sales_unit':("Inv_Item_Sales_Units_v a",
                """a.IIM_ITEM_ID ITEM_ID,a.SU_ID,a.SALES_UNIT,a.SU_NAME,
                a.SU_NUMBER,a.UOM_ID,a.MARKUP,a.PRICE_EXLTAX,a.PRICE_INCTAX,
                a.ATTRIBUTE1,a.ATTRIBUTE2,a.BIN_IDENTIFIER,a.BU_ID,a.CREATE_TYPE,
                a.PRINT_IN_DIRECTORY,a.PRINT_IN_PRICELIST,a.Last_Update_Date,a.Delete_Flag """,
                ' EXISTS   (select NULL from  inv_itemsCantoWWW_v x Where x.Item_Id = a.IIM_Item_ID)  ',
                        ' a.IIM_Item_ID,a.Sales_Unit','item_sales_units.json',''),
    'item_price':("inv_item_price_types_va a",
                """a.IIM_ITEM_ID ITEM_ID,a.IISU_SU_ID SU_ID,a.IPT_PRICE_TYPE_ID PRICE_TYPE_ID,a.ITEM_PRICE_ID,
                a.CURRENCY_CODE,a.PRICE_EXLTAX,a.PRICE_INCTAX,a.PRICE_MARKUP,
                a.BU_ID,a.MARKUP,a.PRICE_TYPE_DISP,a.Last_Update_Date,a.Delete_Flag """,
                ' EXISTS   (select NULL from  inv_itemsCantoWWW_v x Where x.Item_Id = a.IIM_Item_ID)  ',
                        ' a.IIM_Item_ID,a.IISU_SU_ID,a.IPT_PRICE_TYPE_ID ','item_prices.json',''),
    'item_barcode':("inv_item_barcodes_v a",
                """a.IIM_ITEM_ID ITEM_ID,a.IISU_SU_ID SU_ID,
                a.Item_Sl_No, a.Sl_No,a.barcode,a.description,
                a.Price_ExlTax,a.Price_Inctax,a.primary_flag, a.Purchase_Qty,a.Sales_Qty
               ,a.Last_Update_Date,a.Delete_Flag """,
                ' EXISTS   (select NULL from  inv_itemsCantoWWW_v x Where x.Item_Id = a.IIM_Item_ID)  ',
                        ' a.IIM_Item_ID,a.IISU_SU_ID,a.barcode ','item_barcodes.json',''),
    'price_break':("REP_ITEMPRICEBREAK_V a",
                """a.ITEM_ID,a.PRICE_BREAK_ID,a.PRICE_BREAK_LINE_ID,a.NAME,a.SL_NO,
                    a.LINE_USERDISPLAYTEXT,a.QTY_FROM_SOURCE,a.QTY_FROM,a.QTY_TO,a.QTY_TO_SOURCE,
                    a.DATE_FROM,a.DATE_TO,a.DESCRIPTION,a.IPT_PRICE_TYPE_ID PRICE_TYPE_ID,
                    a.PRICE_BREAK_SOURCE_TYPE,a.PRICE_BREAK_TYPE,a.PRICE_BREAK_VALUE,
                    a.SALES_UNIT,a.UPDATE_SOURCE,a.USER_DISPLAY_TEXT
                   ,a.Last_Update_Date,a.Delete_Flag """,
                ' EXISTS   (select NULL from  inv_itemsCantoWWW_v x Where x.Item_Id = a.Item_ID)  ',
                        ' a.ITEM_ID,a.PRICE_BREAK_ID,a.SL_NO ','price_break.json',''),
    'price_breal_text':("inv_itemsCantoWWW_v a",
                """a.ITEM_ID,a.Item_Number,a.Item_Name,
                Price_Pkg.Get_PriceBreakText(a.IPBH_PRICE_BREAK_ID,
                a.item_Id,inv_Pkg.Get_SingleSUID(a.item_Id),1,1) PriceBreak """,
                ' 1 = 1  ',
                        ' a.item_ID ','price_break_text.json',''),
    'customer_fixed_price':("AR_CUSTOMERFIXEDPRICE_V a",
                """a.ITEM_ID,a.ITEM_NAME,a.ITEM_NUMBER, a.ACTIVE,
                    a.CUSTOMER_ID,a.CUSTOMER_NAME,a.CUSTOMER_NUMBER
                    ,a.MIN_QTY,a.MIN_QTY_SOURCE,a.OVERHEAD_PRICE,a.PRICE,a.PRICE_LIST_ID,
                    a.PRICE_TYPE,a.PRICE_TYPE_ID,a.PRICE_TYPE_NAME,
                    a.START_DATE_ACTIVE,a.END_DATE_ACTIVE
                   ,a.Last_Update_Date,a.Delete_Flag """,
                ' EXISTS   (select NULL from  inv_itemsCantoWWW_v x Where x.Item_Id = a.Item_ID)  ',
                        ' a.ITEM_ID,a.customer_Id ','customer_fixed_price.json',''),
}
def export_qtyinstock(p_connection,
                    p_hint:str = 'FULL',
                    p_qtypercent:int = 80,
                    p_includeBOM:str = 'N',
                    p_forwhom:str ="null"):
    vIdentifier = 'QUANTITY IN STOCK 01';
    vCustomerId = "null"
    vLastRundate = "null";
    vctr = 0;

    sql = """
            SELECT Item_Id,Item_Number,decode(derived_salesunit,0,1,derived_salesunit) derived_salesunit,  
                   ceil(floor(
                   (case when qtyinstock < 0 Then 0 else qtyinstock end)
                         /decode(derived_salesunit,0,1,derived_salesunit)
                        )*(80/100))  qtyinstock,
                   qty_balance,promised_date,qty_sold,last_sold_date,item_status,
                   active_flag,min_qty,reorder_qty,max_qty,
                   primarybarcode,bin_identifier,
                     ceil(floor(
                   (case when QtyInStockFull < 0 Then 0 else qtyinstock end)
                         /decode(derived_salesunit,0,1,derived_salesunit)
                        )*(80/100)) qtyinstockfull
            FROM (
            select i.Item_ID,i.Item_Number,
                nvl(Price_Pkg.Get_ItemQuantity('WEBSITE',i.Item_ID,Null,1,null,null),0) Derived_SalesUnit,
                 ITemStatus_Pkg.GetQtyInStock(i.Item_Id,i.Bu_Id) QtyInStock,
                 po.Qty_Balance, po.Promised_Date,iis.Qty_Sold, iis.Last_Sold_Date,i.Item_Status,
                 Decode(i.Item_Status,'ACTIVE','1','0') Active_Flag , i.Min_Qty, i.Reorder_Qty, i.Max_Qty,
                 Inv_Pkg.Get_ItemBarcode('PRIMARY',i.Item_Id) PrimaryBarcode,'NA' Bin_Identifier,
                 nvl(ITemStatus_Pkg.GetQtyInStock(i.Item_Id,Null,i.Bu_Id,'BULEVEL','FULL'),0) QtyInStockFull
           From  Inv_Item_Masters_V i ,
                 (Select poi.Item_ID, nvl(Min(poi.Qty_Balance),0) Qty_Balance ,
                     Min(poi.LinePromised_Date) Promised_Date
                  from REP_ITEMINPO_V poi
                  Group By poi.Item_ID) po,
                  inv_Item_statuses iis 
           Where i.Item_Id = po.Item_ID (+) 
           And  i.Item_ID = iis.item_Id (+) 
           And  Exists ( Select 1
                         From   Cmn_WebsiteItems_V w
                         where w.item_id = i.item_id
                        ) )                        
          """
    print(sql)
    df = pd.read_sql(sql,con=p_connection)
    return df

def export_data_to_json( p_connection,
                        p_table:str = 'ALL',
                        p_tables:{} = WEB_EXPORT
                      ):
    print(p_table)
    for i in p_tables.keys():
        if p_table == 'TABLES' or p_tables == 'ALL' or p_table  in i:
            tablename, columns, where, orderby,file, _ = p_tables[i]
            df = pd.read_sql("""SELECT {} 
                            FROM {} 
                            WHERE {} 
                            ORDER BY {}""".format(columns,tablename,where,orderby), con=p_connection)
            print(df.columns)
            df.to_json(cn_config.OUTBOUND_DIRECTORY + file, orient='records')
    if p_table == 'ALL' or p_table == 'QTYINSTOCK':
        df = export_qtyinstock(p_connection)
        file = 'qtyinstock.json'
        df.to_json(cn_config.OUTBOUND_DIRECTORY + file, orient='records')

def export_qtyinstock(p_connection,
                    p_hint:str = 'FULL',
                    p_qtypercent:int = 80,
                    p_includeBOM:str = 'N',
                    p_forwhom:str ="null"):
    vIdentifier = 'QUANTITY IN STOCK 01';
    vCustomerId = "null"
    vLastRundate = "null";
    vctr = 0;

    sql = """
            SELECT Item_Id,Item_Number,decode(derived_salesunit,0,1,derived_salesunit) derived_salesunit,  
                   nvl(ceil(floor(
                   (case when qtyinstock < 0 Then 0 else qtyinstock end)
                         /decode(derived_salesunit,0,1,derived_salesunit)
                        )*(80/100)),0)  qtyinstock,
                   qty_balance,promised_date,qty_sold,last_sold_date,item_status,
                   active_flag,min_qty,reorder_qty,max_qty,
                   primarybarcode,bin_identifier,
                    nvl(ceil(floor(
                   (case when QtyInStockFull < 0 Then 0 else qtyinstock end)
                         /decode(derived_salesunit,0,1,derived_salesunit)
                        )*(80/100)),0) qtyinstockfull
            FROM (
            select i.Item_ID,i.Item_Number,
                nvl(Price_Pkg.Get_ItemQuantity('WEBSITE',i.Item_ID,Null,1,null,null),0) Derived_SalesUnit,
                 nvl(ITemStatus_Pkg.GetQtyInStock(i.Item_Id,i.Bu_Id),0) QtyInStock,
                 po.Qty_Balance, po.Promised_Date,iis.Qty_Sold, iis.Last_Sold_Date,i.Item_Status,
                 Decode(i.Item_Status,'ACTIVE','1','0') Active_Flag , i.Min_Qty, i.Reorder_Qty, i.Max_Qty,
                 Inv_Pkg.Get_ItemBarcode('PRIMARY',i.Item_Id) PrimaryBarcode,'NA' Bin_Identifier,
                 nvl(ITemStatus_Pkg.GetQtyInStock(i.Item_Id,Null,i.Bu_Id,'BULEVEL','FULL'),0) QtyInStockFull
           From  Inv_Item_Masters_V i ,
                 (Select poi.Item_ID, nvl(Min(poi.Qty_Balance),0) Qty_Balance ,
                     Min(poi.LinePromised_Date) Promised_Date
                  from REP_ITEMINPO_V poi
                  Group By poi.Item_ID) po,
                  inv_Item_statuses iis 
           Where i.Item_Id = po.Item_ID (+) 
           And   Decode('{}','N',Nvl(Item_Dimension,'N'),'Y') = Decode('{}','N','N','Y') 
           And   ( '{}' is null 
                  or 
                i.Item_Id in (Select sl.Item_Id from Inv_Item_Sub_Locations sl 
                              where sl.last_Update_Date >= Nvl({},sl.Last_Update_Date) 
                              UNION
                              Select b.Parent_Item_ID from Inv_BOM b
                              Where  b.Item_ID  in (Select sl.Item_Id from Inv_Item_Sub_Locations sl 
                              where sl.last_Update_Date >= Nvl({},sl.Last_Update_Date) )
                              and   '{}' = 'Y' 
                              )
                ) 
           And  i.Item_ID = iis.item_Id (+) 
           And  Exists ( Select 1
                         From   Cmn_WebsiteItems_V w
                         Where  w.Customer_Number = {}
                         And    {}  is not Null
                         Union all
                         Select 1
                         From   Dual
                         Where  {} is null
                        ) )                        
          """.format(p_includeBOM, p_includeBOM,vLastRundate,vLastRundate,
                     vLastRundate, p_includeBOM,p_forwhom,p_forwhom,p_forwhom)
    print(sql)
    df = pd.read_sql(sql,con=p_connection)
    return df
