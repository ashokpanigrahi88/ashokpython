import os
from os import (environ, path)
import pandas as pd
from oratechetl import (utilconfig, etl_settings)

EXPORT_BASE_DIR = 'exportbase'
IMPORT_BASE_DIR = 'importbase'
STAGE_BASE_DIR = 'stagebase'
DEFAULT_JSON_ORIENT = 'records'
DATA_IMPORT_SOURCE = {
    'what_warehouse': {
        'countries': ("cmn_countries a",
                      """ a.* """,
                      '1 = 1', ' 1 ', 'countries.json', 'a.COUNTRY_CODE'),
        'languages': ("cmn_languages a",
                      """ a.* """,
                      '1 = 1', ' 1 ', 'languages.json', 'a.LANGUAGE_CODE'),
        'currencies': ("cmn_currencies a",
                       """ a.* """,
                       '1 = 1', ' 1 ', 'currencies.json', 'a.CURRENCY_CODE'),
        'currency_rates': ("cmn_currency_rates a",
                           """ a.* """,
                           '1 = 1', ' 1 ', 'currency_rates.json',
                           "a.FROM_CURRENCY_CODE||':'||a.CURRENCY_RATE_DATE||':'||a.TO_CURRENCY_CODE"),
        'companies': ("cmn_companies a",
                    """ a.* """,
                    '1 = 1', ' 1 ', 'companies.json', 'a.COMP_ID'),
        'bsuinessunits': ("cmn_business_units a, cmn_companies b",
                         """ a.*, b.comp_name """,
                         '1 = 1  and a.cc_comp_id = b.comp_id', ' 1 ', 'businessunits.json', 'a.BU_ID'),
        'payment_methods': ("cmn_payment_methods a",
                            """ a.* """,
                            '1 = 1', ' 1 ', 'payment_methods.json', 'a.PMNT_METHOD_ID'),
        'payment_terms': ("cmn_payment_terms a",
                          """ a.* """,
                          '1 = 1', ' 1 ', 'payment_terms.json', 'a.CPT_ID'),
        'seasons': ("cmn_seasons a",
                    """ a.* """,
                    '1 = 1', ' 1 ', 'seasons.json', 'a.SEASON_CODE_ID'),
        'uoms': ("cmn_unit_of_measurements a",
                """ a.* """,
                '1 = 1', ' 1 ', 'uoms.json', 'a.UOM_ID'),
        'gl_categories': ("gl_categories a",
                          """ a.* """,
                          '1 = 1', ' 1 ', 'gl_categories.json', 'a.gl_category_id'),
        'gl_sub_categories': ("gl_sub_categories a, gl_categories b",
                              """ a.*, b.gl_category_name """,
                              """1 = 1 and a.gc_gl_category_id = b.gl_category_id""", ' 1 ',
                              'gl_sub_categories.json', 'a.gl_sub_category_id'),
        'gl_account_codes': ("gl_account_codes a",
                             """ a.* """,
                             '1 = 1', ' 1 ', 'gl_account_codes.json', 'a.gl_account_id'),
        'locations': ("inv_locations a",
                      """ a.* """,
                      '1 = 1', ' 1 ', 'locations.json', 'a.location_id'),
        'categories': ("inv_item_categories a",
                     """ a.* """,
                     '1 = 1', ' 1 ', 'categories.json', 'a.category_id'),
        'sub_categories': ("inv_item_categories a, inv_item_sub_categories b ",
                         """  a.category_name, b.* """,
                    """1 = 1
                    And a.category_id = b.iic_category_id """, '1', 'sub_categories.json', 'b.sub_category_id'),
        'tax_codes': ("cmn_tax_codes a "
                      "LEFT OUTER JOIN gl_account_codes b on a.gac_gl_account_id = b.gl_account_id ",
                     """ a.*, b.gl_account_code """,
                     """1 = 1
                      """, '1', 'tax_codes.json', 'a.tax_code_id'),
        'customer_profiles': ("""ar_customer_profiles a
                            LEFT OUTER JOIN cmn_payment_terms b on a.cpt_cpt_id = b.cpt_id""",
                     """  a.*, b.terms_days """, '1 = 1', ' 1 ', 'customer_profiles.json', 'a.cust_profile_id'),
        'customers': ("""ar_customers_v a 
                        INNER JOIN ar_customer_profiles b on a.ctp_cust_profile_id = b.cust_profile_id 
                        LEFT OUTER JOIN  cmn_tax_codes c on c.tax_code_id = a.ctc_tax_code_id
                        LEFT OUTER JOIN  cmn_payment_terms d on d.cpt_id = a.cpt_cpt_id
                        """,
                     """  a.* , b.cust_profile_name, c.tax_code, c.tax_rate, d.terms_days """,
                      '1 = 1', ' 1 ', 'customers.json', 'a.customer_id'),
        'manufacturers': ("inv_manufacturers_v a",
                         """ a.* """,
                         '1 = 1', '1', 'manufacturers.json', 'a.manf_id'),
        'supplier_profiles': ("ap_supplier_profiles a",
                     """  a.* """, '1 = 1', ' 1 ', 'supplier_profiles.json', 'a.sup_profile_id'),
        'suppliers': (""" ap_suppliers_v a
                       INNER JOIN ap_supplier_profiles b on a.asp_sup_profile_id = b.sup_profile_id 
                        LEFT OUTER JOIN  cmn_tax_codes c on c.tax_code_id = a.ctc_tax_code_id """,
                      """ a.*, b.sup_profile_name , c.tax_code, c.tax_rate """,
                      """ 1 = 1 """, '1', 'suppliers.json', 'a.supplier_id'),
        'cust_fixed_price': ("AR_CUSTOMERFIXEDPRICE_V a",
                             """ a.CUSTOMER_ID,a.CUSTOMER_NAME,a.CUSTOMER_NUMBER,a.ACTIVE,a.BU_ID,
                            a.START_DATE_ACTIVE,a.END_DATE_ACTIVE
                            ,a.ITEM_ID,a.ITEM_NAME,a.ITEM_NUMBER,a.MIN_QTY,a.MIN_QTY_SOURCE,a.OVERHEAD_PRICE
                            ,a.PRICE,a.PRICE_LIST_ID,a.PRICE_TYPE,a.PRICE_TYPE_ID,
                            a.PRICE_TYPE_NAME,a.Last_Update_Date,a.Delete_Flag """,
                             ' EXISTS   (select NULL from  inv_itemsCantoWWW_v x Where x.Item_Id = a.Item_ID)  ',
                             ' a.Customer_Id,a.Item_ID', 'cust_fixed_prices.json',
                             "a.customer_id||':'||a.item_id"),
        'cust_balances': ("rep_customerbalance_v a",
                         """ a.* """,
                         ' 1 = 1 ', '1', 'cust_balances.json', "a.customer_id"),
        'items': ("""inv_item_masters_v a
                 INNER JOIN inv_item_sub_categories c on c.sub_category_id = a.iisc_sub_category_id  
                 INNER JOIN inv_item_categories b on b.category_id = c.iic_category_id
                 INNER JOIN cmn_tax_codes d on d.tax_code_id = a.ctc_tax_code_id
                 INNER JOIN ap_suppliers e on e.supplier_id = a.sup_supplier_id
                 LEFT OUTER JOIN cmn_unit_of_measurements f on f.uom_id = a.uom_id
                 LEFT OUTER JOIN inv_price_break_headers g on g.price_break_id = a.ipbh_price_break_id
                 LEFT OUTER JOIN inv_manufacturers h on h.manf_id = a.im_manf_id""",
                 """ a.*, b.category_name, c.sub_category_name, d.tax_code, d.tax_rate,
                  e.supplier_name, e.supplier_number, f.uom_short_desc, f.uom_long_desc, 
                  g.name price_break_name, h.manf_name, h.manf_number """,
                 " 1 =1 and a.item_number is not null  and a.item_number  Not like '*%'  ", ' 1 ', 'items.json', 'a.item_id'),
        'item_hins': ("inv_itemwebhints_v a",
                      """ a.* """,
                      ' 1 = 1 ', '1', 'item_hints.json', 'a.item_id'),
        'item_infos': (" cmn_additional_info_v a",
                      """ a.* """,
                      " Info_Source = 'inv_item_masters' ", '1', 'item_infos.json', 'a.info_id'),
        'item_sales_units': ("""inv_item_sales_units_v a 
                            INNER JOIN inv_item_masters b on b.item_id = a.iim_item_id
                            LEFT OUTER JOIN cmn_unit_of_measurements c on c.uom_id = a.uom_id
                            LEFT OUTER JOIN inv_item_prices_flat_v d on d.su_id = a.su_id and d.iim_item_id = a.iim_item_id
                                """,
                            """ a.*, b.item_number, b.item_name, c.uom_short_desc, c.uom_long_desc,
                            d.sp1_inctax,d.sp1_exltax,d.sp1_markup, d.sp2_inctax,d.sp2_exltax,d.sp2_markup, 
                            d.sp3_inctax,d.sp3_exltax,d.sp3_markup, d.sp4_inctax,d.sp4_exltax,d.sp4_markup, 
                            d.sp5_inctax,d.sp5_exltax,d.sp5_markup
                             """,
                            """ 1=1 and a.su_number is not null and a.sales_unit is not null
                            and a.su_number  Not like '*%'  """, ' a.iim_item_id,a.sales_unit', 'item_sales_units.json', 'a.su_id'),
        'item_prices': ("inv_item_price_types_va a ",
                       """ a.* """,
                       ' 1 =2  ', ' a.iim_item_id,a.iisu_su_id,a.ipt_price_type_id ', 'a.item_prices.json',
                       'a.ipt_price_type_id'),
        'item_barcodes': ("""inv_item_barcodes_v a 
                            INNER JOIN inv_Item_masters b on b.item_id = a.iim_item_id
                            INNER JOIN inv_item_sales_units c on c.su_id = a.iisu_su_id and c.iim_item_id = a.iim_item_id""",
                         """ a.*, rownum barcode_id,  b.item_number, b.item_name, c.su_number, c.su_name, c.sales_unit """,
                         """ 1=1 and c.su_number is not null and c.sales_unit is not null
                            and c.su_number  Not like '*%'  """, ' a.iim_item_id, a.iisu_su_id,a.barcode ', 'item_barcodes.json', 'a.barcode'),
        'item_multi_categories': ("inv_item_multi_categories a ",
                                  """ a.* """,
                                  ' 1 = 1  ', ' 1', 'item_multi_categories.json', "a.item_id||':'||a.sub_category_id"),
        'item_similar_categories': ("inv_similar_categories a ",
                                    """ a.* """,
                                    ' 1 = 1  ', '1 ', 'item_similar_categories.json', "similar_category_id"),
        'item_boms': ("inv_bom a ",
                     """ a.* """,
                     ' 1 = 1  ', ' 1 ', 'item_boms.json', 'a.bom_id'),
        'item_multi_seasons': ("inv_item_multi_seasons a",
                                """ a.* """,
                                ' 1 = 1  ', ' 1', 'item_multi_seasons.json', 'a.multi_season_id'),
        'price_breaks': ("REP_ITEMPRICEBREAK_V a ",
                        """ a.* """,
                        ' 1=1  ', ' ITEM_ID,PRICE_BREAK_ID, SL_NO ', 'price_breaks.json',
                        "ITEM_ID||':'||PRICE_BREAK_ID||':'|| SL_NO"),
        'price_breal_texts': ("inv_itemsCantoWWW_v a",
                             """a.ITEM_ID,a.Item_Number,a.Item_Name,
                            Price_Pkg.Get_PriceBreakText(a.IPBH_PRICE_BREAK_ID,
                            a.item_Id,inv_Pkg.Get_SingleSUID(a.item_Id),1,1) PriceBreak """,
                             ' 1 = 1  ',
                             ' a.item_ID ', 'price_break_texts.json', "a.item_id"),
        'customer_fixed_prices': ("AR_CUSTOMERFIXEDPRICE_V a",
                                 """a.ITEM_ID,a.ITEM_NAME,a.ITEM_NUMBER, a.ACTIVE,
                                    a.CUSTOMER_ID,a.CUSTOMER_NAME,a.CUSTOMER_NUMBER
                                    ,a.MIN_QTY,a.MIN_QTY_SOURCE,a.OVERHEAD_PRICE,a.PRICE,a.PRICE_LIST_ID,
                                    a.PRICE_TYPE,a.PRICE_TYPE_ID,a.PRICE_TYPE_NAME,
                                    a.START_DATE_ACTIVE,a.END_DATE_ACTIVE
                                   ,a.Last_Update_Date,a.Delete_Flag """,
                                 ' 1=1  ', ' a.ITEM_ID,a.customer_Id ',
                                 'customer_fixed_prices.json',
                                 "a.item_id||':'||a.customer_Id "),
        'location_stocks': ("""Inv_Item_Masters_V  a , 
                                            (Select poi.Item_ID, nvl(Min(poi.Qty_Balance),0) Qty_Balance ,
                                            Min(poi.LinePromised_Date) Promised_Date
                                            from REP_ITEMINPO_V poi
                                            Group By poi.Item_ID) po,
                                            inv_Item_statuses iis """,
                           """a.Item_ID,a.Item_Number,
                          nvl(Price_Pkg.Get_ItemQuantity('WEBSITE',a.Item_ID,Null,1,null,null),0) Derived_SalesUnit,
                           ITemStatus_Pkg.GetQtyInStock(a.Item_Id,a.Bu_Id) QtyInStock,
                           po.Qty_Balance, po.Promised_Date,iis.Qty_Sold, iis.Last_Sold_Date,a.Item_Status,
                           Decode(a.Item_Status,'ACTIVE','1','0') Active_Flag , a.Min_Qty, a.Reorder_Qty, a.Max_Qty,
                           Inv_Pkg.Get_ItemBarcode('PRIMARY',a.Item_Id) PrimaryBarcode,'NA' Bin_Identifier,
                           nvl(ITemStatus_Pkg.GetQtyInStock(a.Item_Id,Null,a.Bu_Id,'BULEVEL','FULL'),0) QtyInStockFull
                             ,a.Last_Update_Date,a.Delete_Flag """,
                           """ 1=1 
                              and a.Item_Id = po.Item_ID (+) 
                              And  a.Item_ID = iis.item_Id (+)  """, " a.item_id ",
                           'location_stocks.json',
                           " a.item_id "),
    },
    'what_nuepos': {
        'manufacturers': (" FROM ProductManufacturers a",
                                 """ SELECT a.ManufacturerName manf_name, SUBSTRING(a.ManufacturerName,1,20) manf_short_name,-99 manf_id,
       'UK' country_code, NULL contact_name, a.ManufacturerURL www, a.ManufacturerContactNumber mobile,
       a.ManufacturerEmail email, a.ManufacturerContactNumber fax, a.ManufacturerContactNumber phone1,
       null phone2, a.ManufacturerPostalCode post_code, a.ManufacturerAddress address_line1,
       SUBSTRING(a.ManufacturerName,1,25) manf_number,  a.ManufacturerNotes attribute1, null attribute2, null mkuptemp_id """,
                                 'WHERE 1 = 1 and a.DELETED IS NULL ', ' ORDER BY 1 ', 'manufacturers.json', '  a.RowGUID '),
        'suppliers': ("FROM Suppliers a",
                      """  SELECT a.SupplierName supplier_name, SUBSTRING(a.SupplierName,1,20) short_name,-99 supplier_id,
        a.SupplierRepName contact_name, a.SupplierAccountNumber account_number, a.SupplierMinimumOrder min_order_amount,
         Null www, SUBSTRING(a.SupplierContactNumber1,1,20) mobile,
       a.SupplierEmail email, SUBSTRING(a.SupplierFaxNumber,1,20) fax, SUBSTRING(a.SupplierContactNumber1,1,20) phone1,
       SUBSTRING(a.SupplierContactNumber2,1,20) phone2, a.SupplierPostalCode post_code, a.SupplierAddress address_line1,
       SUBSTRING(a.SupplierName,1,20) supplier_number,  a.SupplierNotes attribute1, null attribute2, 1 asp_sup_profile_id,
       'GENERAL' sup_profile_name,
       null ctc_tax_code_id, 'T1' tax_code, 'GBP' currency_code, 'UK' country_code, null cpt_id, 'IMMEDIATE' terms_name,
        null pmnt_method_id , 'BACS' pmnt_method""",
                      """ WHERE 1 = 1 and  a.Deleted is NULL and   a.SupplierName != '-' """, ' ORDER BY 1 ', 'suppliers.json', '  a.RowGUID '),
        'categories': (" FROM  ProductCategories a",
                     """ SELECT distinct a.CategoryName category_name, a.CategoryNotes key_words,
                     a.FullQualifiedName description,  '-99' category_id """,
                     """ WHERE a.ParentCategory is NULL and a.Deleted is NULL """, ' ORDER BY 1 ', 'categories.json', ' a.RowGUID '),
        'sub_categories': (" FROM  ProductCategories a, ProductCategories b ",
                         """  SLEECT distinct a.CategoryName category_name, b.CategoryName sub_category_name,  b.CategoryNotes key_words,
                         b.FullQualifiedName description,  -99  sub_category_id  """,
                         """ WHERE a.ParentCategory is NULL and a.Deleted is NULL
                            And     b.ParentCategory = a.RowGUID
                            and     b.Deleted is NULL 
                            and     b.CategoryName != '-' """, ' ORDER BY 1,2 ', 'sub_categories.json', ' b.RowGUID '),
        'item_barcodes': (" FROM ProductBarcodes a",
                            """ SLEECT a.* """,
                            '1 = 1 and a.DELETED IS NULL ', ' 1 ', 'item_barcodes.json', ' a.RowGUID '),
        'productlinkedquantities': ("ProductLinkedQuantities a",
                                    """ a.* """,
                                    '1 = 1 and a.DELETED IS NULL ', ' ORDER BY 1 ', 'product_linkedqty.json', ' a.RowGUID '),
        'customers': (""" FROM Customers a 
                LEFT OUTER JOIN CustomerAddresses b on b.CustomerGUID = a.RowGUID and b.RowGUID = a.InvoiceAddress 
                LEFT OUTER JOIN ( Select mi.CustomerGUID customerid, mi.RowGUID  mobileid , max(mi.PhoneNumber) mobile 
                  From CustomerPhoneNumbers mi
                  GROUP BY mi.CustomerGUID, mi.RowGUID ) m on m.customerid = a.RowGUID  and m.mobileid = a.MobilePhoneGUID
                LEFT OUTER JOIN ( Select p1i.CustomerGUID customerid, p1i.RowGUID  phone1id , max(p1i.PhoneNumber) phone1 
                  From CustomerPhoneNumbers p1i
                  GROUP BY p1i.CustomerGUID, p1i.RowGUID ) p1 on p1.customerid = a.RowGUID  and p1.phone1id = a.HomePhoneGUID
                LEFT OUTER JOIN ( Select p2i.CustomerGUID customerid, p2i.RowGUID  phone2id , max(p2i.PhoneNumber) phone2
                  From CustomerPhoneNumbers p2i
                  GROUP BY p2i.CustomerGUID, p2i.RowGUID ) p2 on p2.customerid = a.RowGUID  and p2.phone2id = a.WorkPhoneGUID
                    """,
                      """ SELECT 0 balance , a.CreditLimit cust_credit_limit , a.EmailAddress   email  , null fax  , 
                      null phone2  , p1.phone1 phone1  , SUBSTRING(REPLACE(upper(a.FullName),' ',''),1,20) customer_number  ,
  b.PostalCode billto_post_code  , 'UK' billto_country_code  ,  
   CONCAT(b.BuildingName,' ', b.AddressLine1) billto_address_line1  , 
   a.FullName contact_full_name  , ISNULL(a.CompanyName, a.FullName) customer_name  , 
   a.FirstName contact_forename  , a.LastName contact_surname , 
   a.Title cust_title  , -99 customer_id , 'GBP' currency_code  , 'IMPORT' update_source  , null cust_vatregno  , 
   a.NoPoints attribute2  , a.NoMarketing attribute1  , 
   'I' record_status  , 1 last_updated_by  , a.CreditLimit last_update_date  , 
   null login_name  , null cust_password  , 0 paid_amount  , 0 invoiced_amount  , 
   a.DateAdded creation_date  , 1 created_by  , 'N' delete_flag  , b.Locality  billto_county  , 
   b.AddressLine2 billto_city  , 'UK' shipto_country_code  ,
    b.Locality shipto_county  , b.AddressLine2 shipto_city  , b.PostalCode shipto_post_code  , 
    CONCAT(b.BuildingName,' ', b.AddressLine1) shipto_address_line1   , 
    null gl_account_id  ,     null orig_system_ref_hdr  , null orig_system_ref  , null primary_customer_id  , 
    null ipt_price_type_id  , null customer_pricename  , null cpt_cpt_id  , 
     null ctp_cust_profile_id  , 1 ctc_tax_code_id  , null min_deposit_amount  , 
     'N' take_deposit  , 'N' reserve_item  , null www   , 
     null customer_markupdown  , null hold_reason  , null customer_hold  , 1 bu_id  , m.mobile mobile  , 
     null pmnt_method_id  , null freight_line_id  , 
     null freight_header_id  , null location_id  , null item_pop_method  , null min_item_su_value  , null min_item_su_type  , 
     null customer_class_code  , 'N' upload_items  , null max_value  , null min_value  , null customer_category  , null host_image_path2  ,
     null picturetype  , null picturename  , 'N' account_allowed  , 'Y'  print_customer_name  , 
      'Y' consolidate_items  , 'N' upload_instock_items  , a.NoMarketing www_subscription_preference  , null www_end_date  , 
      null www_start_date  , null www_customer_category  , null www_min_order_freeship  , null www_price_break_display  , 
      null www_min_order_value  , null www_price_type_id  , null www_markupdown  , null supplier_id  , null customer_type_code  ,
       null rrp_percentage  , null export_customer  , null job_id  , null shipto_address_type  , null export_column_list  , 
       null export_footer  , null export_header  , null export_header_list  , null item_batch_id  , null backorder_header_id  ,
      null filter_criteria  , null item_batch_hint  , null date_format  , null default_upload_status  ,
      null www_sub_source_id  , null language_code  , null print_price_type_id, 'BYORDER' www_shipping_hint, 'N' www_price_incshipping  , 
      null price_import_hint,'FROMFILE' shipto_email  , null shipto_contact_name  , null price_invoice_hint  ,
       null eori_number,'CASH CUSTOMER' cust_profile_name,'T1' tax_code, 20.0 tax_rate,0 terms_days """,
                      ' WHERE 1 = 1 and a.DELETED IS NULL ', ' ORDER BY 1 ', 'customers.json', ' a.RowGUID '),
        'customercards': (" FROM CustomerLinkedCards a",
                          """ SELECT a.* """,
                          'WHERE 1 = 1 and a.DELETED IS NULL ', ' ORDER BY 1 ', 'customer_cards.json', ' a.RowGUID '),
        'customerpoints': ("FROM CustomerPoints a",
                           """ SELECT a.* """,
                           'WHERE 1 = 1 and a.DELETED IS NULL ', ' ORDER BY 1 ', 'customer_points.json', ' a.RowGUID '),
        'specialoffers': (" FROM SpecialOffers a",
                          """ SELECT a.* """,
                          'WHERE 1 = 1 and a.DELETED IS NULL ', ' ORDER BY 1 ', 'special_offers.json', ' a.RowGUID '),
        'items': ("",
                           """
                           WITH all_barcodes
                  AS (
                  /* -- pivot rows to columns the barcodes  */
                  Select ROW_NUMBER() OVER( PARTITION by b.StockGUID   ORDER BY b.StockGUID ASC, b.PrimaryBarcode DESC  ) AS rownum, 
                     Case  ROW_NUMBER() OVER( PARTITION by b.StockGUID   ORDER BY b.StockGUID ASC , b.PrimaryBarcode DESC    )
                     When 1 then barcode else null end primary_barcode,
                     Case ROW_NUMBER() OVER( PARTITION by b.StockGUID   ORDER BY b.StockGUID ASC , b.PrimaryBarcode DESC    )
                     When 2 then barcode else null end barcode2,
                     Case ROW_NUMBER() OVER( PARTITION by b.StockGUID   ORDER BY b.StockGUID ASC , b.PrimaryBarcode DESC     )
                     When 3 then barcode else null end barcode3,
                     Case ROW_NUMBER() OVER( PARTITION by b.StockGUID   ORDER BY b.StockGUID ASC , b.PrimaryBarcode DESC    )
                     When 4 then barcode else null end barcode4,
                     Case ROW_NUMBER() OVER( PARTITION by b.StockGUID   ORDER BY b.StockGUID ASC, b.PrimaryBarcode DESC     )
                     When 5 then barcode else null end barcode5,
                      b.*
                  From ProductBarcodes b
                  where b.deleted is null
                  ),
                  barcodes_inrow AS
                  (
                  /* flatten barcodes to single row by product id */ 
                  select ab.StockGUID, max(ab.primary_barcode) primarybarcode , max(barcode2) barcode2 ,
                     max(barcode3) barcode3, max(barcode4) barcode4 , max(barcode5) barcode5
                  from all_barcodes ab
                  Group by ab.StockGUID
                  ),
                  primary_supplier AS
                  ( /* get Primary Suppplier */
                      select ProductGUID, SupplierGUID, count(1) noof_records
                    From ProductSuppliers
                    Where PrimarySupplier = 1
                    and Deleted is null
                    Group by ProductGUID,SupplierGUID
                    having count(1) =1
                    )
                  /* join barcodes , product , category and patent category */
                  select p.RowGUID product_id, bi.primarybarcode, bi.barcode2, bi.barcode3, bi.barcode4, bi.barcode5,
                   p.ProductName, p.AlternativeDisplayName, p.StandardSellingPrice, p.StandardSellingPriceExTax,
                  p.TaxRate, p.RRP, p.Length, p.Width, p.Depth, p.DimensionUnits, p.weight, p.WeightUnits,
                   p.VariablePrice, p.Minimum, p.Maximum, p.LastUpdated, p.Discontinued, p.AgeRestriction,p.DateCreated,
                   p.PointsMultiplier,   parent.RowGUID category_id, parent.CategoryName CategoryName,  parent.FullQualifiedName category_desc,
                  c.RowGUID  sub_category_id,  c.CategoryName Sub_Category, c.FullQualifiedName sub_category_desc ,
                  m.RowGUID manf_id, m.ManufacturerName, s.RowGUID supplier_id, s.SupplierName,
                  'what_nuepos' third_party_source, p.RowGUID third_party_source_ref
                  From Products p 
                  LEFT OUTER JOIN barcodes_inrow bi ON p.RowGUID = bi.StockGUID
                  LEFT OUTER JOIN ProductCategories c ON p.Category = c.RowGUID
                  LEFT OUTER JOIN  ProductCategories parent ON c.ParentCategory = parent.RowGUID 
                  LEFT OUTER JOIN  ProductManufacturers m ON p.Manufacturer = m.RowGUID and m.Deleted is null
                  LEFT OUTER JOIN primary_supplier ps ON p.RowGUID = ps.ProductGUID
                  LEFT OUTER JOIN Suppliers s ON ps.SupplierGUID = s.RowGUID and s.Deleted is null
                  WHERE p.deleted is null And c.Deleted is null  AND  p.Discontinued = 0 ORDER BY p.RowGUID
                   """,
                           ' ', ' ', 'item_details.json', ' p.RowGUID '),
        'item_locations': ("",
                  """
                select 1 TP_SOURCE_ID, NULL TP_STOCK_LINE_ID,  case plq.StoreGUID 
                        When 'a8981ec3-b497-481c-8e69-f19299e820d5' Then upper('Nailsea')
                        When '782840f3-7d26-4916-85c1-1eca8c4f6b5a' Then  UPPER( 'What Rogerstone')
                        When '45f4a9c0-52b5-4f4f-b7ac-853394407255' Then   UPPER('What Eastgate')
                        else 'NOT USED'
                        end location_name,
                        case plq.StoreGUID 
                        When 'a8981ec3-b497-481c-8e69-f19299e820d5' Then 2
                        When '782840f3-7d26-4916-85c1-1eca8c4f6b5a' Then  18
                        When '45f4a9c0-52b5-4f4f-b7ac-853394407255' Then  12
                        else -1
                        end location_id,
                        p.ProductName item_name, 
                        max(b.barcode) barcode, 
                        p.RowGUID source_item_id , plq.StoreGUID location_source_id, sum(plq.Quantity) quantity,
                        max(plq.MovementDate) last_update_date, CONCAT(plq.StoreGUID,':',p.RowGUID) tp_uk
                      from Products p
                      LEFT OUTER JOIN  ProductBarcodes b on p.RowGUID = b.StockGUID and b.PrimaryBarcode = 1 and b.Deleted is NULL
                      inner JOIN  ProductLocationQuantities plq on p.RowGUID = plq.StockGUID 
                                                    and plq.Deleted is NULL
                                                    and plq.StoreGUID in ('a8981ec3-b497-481c-8e69-f19299e820d5','782840f3-7d26-4916-85c1-1eca8c4f6b5a','45f4a9c0-52b5-4f4f-b7ac-853394407255')
                      Where p.Deleted is NULL
                     GROUP BY p.ProductName,case plq.StoreGUID 
                        When 'a8981ec3-b497-481c-8e69-f19299e820d5' Then upper('Nailsea')
                        When '782840f3-7d26-4916-85c1-1eca8c4f6b5a' Then  UPPER( 'What Rogerstone')
                        When '45f4a9c0-52b5-4f4f-b7ac-853394407255' Then   UPPER('What Eastgate')
                        else 'NOT USED' end, p.RowGUID, plq.StoreGUID,
                        case plq.StoreGUID 
                        When 'a8981ec3-b497-481c-8e69-f19299e820d5' Then 2
                        When '782840f3-7d26-4916-85c1-1eca8c4f6b5a' Then  18
                        When '45f4a9c0-52b5-4f4f-b7ac-853394407255' Then  12
                        else -1
                        end 
                    HAVING  sum(plq.Quantity) > 0
          """,
                  ' ', ' ', 'item_locations.json', ' p.RowGUID '),
    } ,
    'what_ecommerce_out': {
        'stores': ("inv_locations a",
                      """a.location_id storeId, a.location_name storeName, a.location_type storeType,
                    a.location_desc storeDescription, 0 storeLatitude, 0 storeLongitude,
                    a.email storeEmailId, a.phone2 storeMobileNo, a.location_contact storeContactPersonName,
                    a.location_area_code storeRegNo,a.address address, a.city state, a.county county,
                    a.post_code zipcode, decode(a.active,'Y','Enable','Disable') status
                    """,
                      '1 = 1', ' 1 ', 'stores.json', 'a.location_id'),
        'store_addresses': ("inv_locations a",
                      """ rownum addressid,'store' entityType , a.location_id entityid,
                     a.address address, a.city state, a.county county,
                    a.post_code zipcode, a.country_code country, 0 lat, 0 lng, decode(a.active,'Y','Enable','Disable') status
                    """,
                      '1 = 1', ' 1 ', 'store_addresses.json', 'a.location_id'),
        'categories': ("Inv_category_hierarchy_v a",
                      """  a.category_id CategoryId, a.category_name categoryname,nvl(a.parent_category_id,0) parentcategoryid, 
                         'No' onHomepage, rownum displayOrder, a.picturename weblink, a.description metatitle, 
                        a.key_words vmcategorytags,  a.key_words meta_keywords, a.attribute2 metadescription, 
                        null smallimageurl, null largeimageurl,'Enable' status
                    """,
                      '1 = 1', ' 1 ', 'categories.json', 'a.category_id'),
        'uoms': ("cmn_unit_of_measurements a ",
                      """ a.uom_id  uomId,  a.uom_short_desc uomSmallDesc, a.uom_long_desc uomLongDesc,
                        a.uom_conversion uomUnit , rownum serialNo, decode(a.active,'Y','Enable','Disable') status
                    """,
                      '1 = 1', ' 1 ', 'uoms.json', 'a.uom_id'),
        'tax_codes': ("cmn_tax_codes a ",
                      """ a.tax_code_id taxId,'VAT' taxType,
                        a.tax_desc taxDescription, a.tax_rate taxPercentage,
                        a.tax_code taxCode, decode(a.delete_flag,'Y','Enable','Disable') status
                    """,
                      '1 = 1', ' 1 ', 'tax_codes.json', 'a.tax_code_id'),
        'products': (""" Inv_Item_Masters a , inv_manufacturers m ,
                            Inv_Item_Sales_Units su """,
                      """a.Item_Id productId,rownum productSlNo,a.Item_name name,m.manf_name brandName,Null make
                        ,Null model,inv_pkg.get_itembarcode('PRIMARY',a.item_id) barCode,
                        a.supplier_product_code vendorBarCode,Null QRCode,Null vendorQRCode
                        ,a.item_number sku,'Item' productType,a.iisc_sub_category_id categoryId, null categoryName,
                        a.key_words productSynonyms,a.short_desc shortDescription
                        ,null linkedProducts,null webLink,rownum displayOrder,-1 stockAvailability,0 stockQuantity
                        ,'Y' shipEnabled,su.sp1_inctax productBasePrice,'SINGLE' defaultUnitType,a.stock_holding_unit defaultUnitQty,
                        su.sp1_inctax defaultPrice
                        ,su.sp1_inctax defaultPriceAfterDiscount,null relatedProducts,null smallImageUrl,ctc_tax_code_id taxMapingId
                        ,decode(a.delete_flag,'Y','Enable','Disable') status 
                    """,
                      """ a.im_manf_id = m.manf_id (+)
                        and   a.item_id = su.iim_item_Id (+)
                        and  nvl(su.sales_unit,1) = 1 """, ' 1 ', 'products.json', 'a.item_id'),
        'product_prices': (""" Inv_Item_Masters a  ,
                            Inv_Item_Sales_Units su """,
                      """a.Item_Id productId,rownum productSlNo,a.Item_name name,inv_pkg.get_itembarcode('PRIMARY',a.item_id) barCode,
                       su.sales_unit,su.sp1_inctax,su.sp1_exltax,su.sp1_markup,
                       su.sp2_inctax,su.sp2_exltax,su.sp2_markup,
                       su.sp3_inctax,su.sp3_exltax,su.sp3_markup,
                       su.sp4_inctax,su.sp4_exltax,su.sp4_markup,
                       su.sp5_inctax,su.sp5_exltax,su.sp5_markup,
                        decode(a.delete_flag,'Y','Enable','Disable') status 
                    """,
                      """  a.item_id = su.iim_item_Id
                       """, ' 1 ', 'product_prices.json', 'a.item_id'),
        'store_quantities': ("inv_locations a, inv_item_locations l, inv_item_masters i",
                      """ a.location_id Storeid, a.location_name StoreName, i.item_id ProductId, i.item_name name,
                      i.Item_Number sku, l.quantity,
                      'Enable' status
                    """,
                    """ a.location_id = l.location_id and l.item_id = i.item_id """, ' 1 ', 'store_quantities.json', 'a.location_id'),
    }
}
"""
productId	productSlNo	name	brandName	make	model	barCode	vendorBarCode (In Array)	QRCode	
vendorQRCode (In Array)	sku	productType	categoryId	categoryName	
productSynonyms (In Array)	shortDescription	linkedProducts (In Array)	webLink	displayOrder	
stockAvailability (Yes/No)	stockQuantity	shipEnabled (Yes/No)	productBasePrice	
defaultUnitType	defaultUnitQty	defaultPrice	defaultPriceAfterDiscount	relatedProducts (In Array)	
smallImageUrl	taxMapingId	fullDescription	sourcing	otherInfo	moreInfo	
eAN	hSN	uPC	productVideo	largeImageUrl (In Array)	status (Enable/Disable)

Products This is the main products table where all other product related details come from.
ProductCategories This is the category tree. Each product can only belong to one category. There is also a table functions to help getting all children which is called GetAllCategoriesWithinCategory.
Suppliers This is a list of all suppliers
ProductSuppliers This is a list of all suppliers that a product can be bought from. Only one primary supplier is allowed per product.  This is where the supplier cost is located. You may also be interested in the function GetIndividualProductSupplierCost, which will calculate the cost based on any linked composition items.
ProductManufactuers A simple table which contains all manufactuers. Each product may only have one manufacturer
ProductLinkedQuantities  This table is for when an item is linked to a parent for purposes of stock levels deduction and cost. Not many products will use this. An example might be weighed up items or a 25ml shot of Jack Daniels. When a shot of JD is sold, the system will take the correct fraction of its parent product. 70cl bottle = 700ml, therefore 25/750 will be deducted from the big bottle.
Do not worry about variations or child items, they are not using them.
ProductLocationQuantities – This contains the stock quantities of each item per product, per location, per store. We support multiple locations in one store, but I don’t think they are using them, so the LocationGUID is simply NULL. The StoreGUID defines which store the record goes to.
The movement type is a number representing why each stock change occurred.

        ProductCreation = 0

        ManuallyEditProduct = 1

        MarkdownProduct = 2

        ProductImport = 3

        Sale = 4

        ReplenishmentIncrease = 5

        ReplenishmentDecrease = 6

        StockTransferTo = 7

        StockTransferFrom = 8

        LinkedItem = 9

        PostSale = 10

        FromBondedRecord = 11

        ManuallyEditProductViaAPP = 12

        IncreasedViaSalesScreen = 13

        DecreasedViaSalesScreen = 14

        ZeroedForStockTake = 15

        ManuallyAdjustQuantityDuringStockTake = 16

        ManuallyAdjustQuantityViaAPPDuringStockTake = 17

        GeneralOrdersDispatched = 18

        ReplenishmentSetStockLevel = 19

        PreReducedProduct = 20



Customers This table contains all the customers. We support multiple addresses and telephone numbers per customer. The customer table names I believe are fairly self explanatory.

CustomerLinkedCards This table contains all the membership numbers, swipe codes etc. to quickly select a customer.

CustomerPoints Similar to productlocationquantities, add up all points to get the total number of points per customer



Special Offers. Special Offers are stored here, and our system supports a wide variety of special offers. There are four primary methods, DiscountBy, DiscountTo, DiscountByPercent and DiscountCheapestPercent. They are checked in order of priority, and support other characteristics as well such as Loyalty Only, Limit Max Per customer etc. The Boolean value MultipleVisitsAllowed, allows customers to buy items over multiple occasions, which is stored in SpecialOffersRepeatPurchaseValues.

SpecialOfferRestrictions These are restrictions that prevent the offer from working during certain times, or based on the selected customer etc.

SpecialOfferGroups Each offer will have at least one group. This tells the system how many items are required. Multiple groups are for meal deals etc.

SpecialOfferItems The items that the customer can buy to qualify for the offer are found here, and they reference the SpecialOfferGroups. Products, categories or manufacturers can be chosen.

Items in the cart are checked for offers using a very sophisticated SQL procedure which is CalculateCartTotal. This is in turn is split up into many parts for simplicity, and is responsible for calculating the final amount. It is ran each time a new product is put into the cart.

When a sale is completed, the procedure CheckAndCompleteTransaction is ran.





DATABASE RULES

1.       Every table has a primary key of RowGUID. This is to ensure the system can work offline and for purposes of synchronisation. Any inserted row is automatically inserted into SyncJobs table which is then processed every 10 seconds so that the computer knows which records have been changed.

2.       Almost EVERY table has a DELETED column. Always write code that excludes any lines that have a value in this column E.G. AND DELETED IS NULL

3.       Never delete records. Always set them to DELETED = GETDATE() if you want to delete them.

4.       Deleted records over 4 weeks old are automatically deleted by the system.

5.       Changes of Permanent Characteristics of Products are stored in AmendmentHistory. If you need this information let me know as all the details are enumerated.

6.       The StoreGUID represents which store the record belongs to. Because all stores (except Tin Can kitchen) share information, a lot of tables have StoreGUID’s that point to Head Office, e.g. Products etc. Those that would be unique to the store e.g. Transactions, Product Location Quantities etc. have the corresponding storeguid’s instead. Since Tin Can Kitchen has separate stock, the stock for this store is configured to point to itself, therefore its StoreGUID is itself. Each store can choose which store each section points to. E.g. some companies don’t share customers across all stores but do share stock etc. Suffice to say, look at records that already exist, and try to copy them.

7.       Tables may have more columns in the future, but I don’t think this should be a problem. All new columns are configured to handle NULLs.

8.       Ignore AccountGUID, and just use the same value 763319aa-ccc0-43a9-9e96-d1642de1b78b whenever inserting a new row. This is the same across the entire database.


 """


def export_qtyinstock(p_connection,
                      p_hint: str = 'FULL',
                      p_qtypercent: int = 80,
                      p_includeBOM: str = 'N',
                      p_forwhom: str = "null",
                      p_filedirectoiry: str = 'export'):
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
    df = pd.read_sql(sql, con=p_connection)
    return df


def read_json_data(p_file: str,
                    p_source: str = 'what_warehouse',
                    p_filedirectory: str = 'exportbase'
                      ):
    v_source = DATA_IMPORT_SOURCE[p_source]
    if os.path.isdir(p_filedirectory):
        file_directory =  utilconfig.get_directory(p_source=p_source, p_basedir=p_filedirectory)
    else:
        file_directory = p_filedirectory
    df = pd.DataFrame()
    tablename, columns, where, orderby,file, indexcol = v_source[p_file]
    if path.exists(file_directory+file):
        df = pd.read_json(file_directory+file,orient=DEFAULT_JSON_ORIENT)
        df.columns = df.columns.str.lower()
        return df, v_source[p_file]
    else:
        return None , v_source[p_file]

def assign_audit_columns(data):
    data['creation_date'] = utilconfig.sysdate()
    data['created_by'] = '-1'
    data['last_updated_by'] = '-1'
    data['update_source'] = 'IMPORT'
    data['record_status'] = 'I'
    data['delete_flag'] = 'N'
    data['last_update_date'] = utilconfig.sysdate()
    return data

def get_auditcolumns(p_type = None):
   columns = """created_by,creation_date,last_updated_by,last_update_date,update_source,delete_flag,record_status"""
   return columns

def formatcolumns(p_columns, p_type = 'bind'):
    retcal = ""
    columns = p_columns
    if not p_type:
        return columns
    if type(columns) !=  type([]):
        print(type(columns),columns)
        columns_array = columns.split(',')
    else:
        columns_array = p_columns
    if p_type == 'bind':
        retval = ','.join([":{}".format(x) for x in columns_array])
    if p_type == '%s':
        retval = ','.join(["%s" for x in columns_array])
    if p_type == '%()s':
        retval = ["%({})s".format(x) for x in columns_array]
        retval = ','.join(retval)
    return retval

def get_auditcolumnvalues():
    return "-1,sysdate,-1,sysdate,'IMPORT','I','N'"


def load_data_in_memory(p_db,p_datasource, p_table:str = None,p_where='default'):
    if p_table is None:
        return pd.DataFrame()
    conn = utilconfig.get_connection(p_db)
    v_where = p_where
    if v_where == 'default':
        v_where = """ and third_party_source = '{}' """.format(p_datasource)
    v_sql = "SELECT * from {} Where 1 = 1 {}".format(p_table,v_where)
    data = pd.read_sql(v_sql,conn)
    data.columns = data.columns.str.lower()
    return data


def is_datasource_valid(p_name):
    if p_name in DATA_IMPORT_SOURCE.keys():
        return True
    return False

def is_database_valid(p_name):
    if p_name in etl_settings.DB_CONNECTIONS.keys():
        return True
    return False

def get_filename_bysource(p_source, p_identifier):
    ## 5th position is file name and index is 4
    v_filename = DATA_IMPORT_SOURCE[p_source][p_identifier][4]
    return v_filename
