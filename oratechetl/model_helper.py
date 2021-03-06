from oratechetl import commonutil
PRIMARY_KEY = {'ApDbnoteHeaders':{'pk':'dbnote_id','uk':'dbnote_number','table':'ap_dbnote_headers'},
'ApInvoiceHeaders':{'pk':'invoice_id','uk':'sup_supplier_id,voucher_num','table':'ap_invoice_headers'},
'ApInvoiceLines':{'pk':'invoice_line_id','uk':'invoice_id,sl_no','table':'ap_invoice_lines'},
'ApPaymentLines':{'pk':'payment_line_id','uk':'payment_header_id,sl_no','table':'ap_payment_lines'},
'ApSuppliers':{'pk':'supplier_id','uk':'supplier_name','table':'ap_suppliers'},
'ApSupplierPriceLists':{'pk':'price_list_id','uk':'item_id,supplier_id','table':'ap_supplier_price_lists'},
'ApSupplierProfiles':{'pk':'sup_profile_id','uk':'sup_profile_name','table':'ap_supplier_profiles'},
'ArCustomers':{'pk':'customer_id','uk':'customer_number','table':'ar_customers'},
'ArCustomerPricelists':{'pk':'customer_pricelist_id','uk':'customer_id,pricelist_header_id',
                        'table':'ar_customer_pricelists'},
'ArCustomerPriceLists':{'pk':'price_list_id','uk':'customer_id,item_id','table':'ar_customer_price_lists'},
'ArCustomerProfiles':{'pk':'cust_profile_id','uk':'cust_profile_name','table':'ar_customer_profiles'},
'ArCustsplitHeaders':{'pk':'custsplit_id','uk':'custsplit_name','table':'ar_custsplit_headers'},
'ArCustsplitLines':{'pk':'custsplit_line_id','uk':'custsplit_id,customer_id','table':'ar_custsplit_lines'},
'ArCustBarcodeUploads':{'pk':'upload_barcode_id','uk':'upload_id,barcode','table':'ar_cust_barcode_uploads'},
'ArCustPaymentMethods':{'pk':'cpm_id','uk':'cust_customer_id,cpm_pmnt_method_id','table':'ar_cust_payment_methods'},
'ArDeliveryHeaders':{'pk':'delivery_header_id','uk':'delivery_note_number','table':'ar_delivery_headers'},
'ArDeliveryLines':{'pk':'delivery_line_id','uk':'delivery_header_id,sl_no','table':'ar_delivery_lines'},
'ArFreightCountries':{'pk':'freight_country_id','uk':'freight_line_id,country_code','table':'ar_freight_countries'},
'ArFreightHeaders':{'pk':'freight_header_id','uk':'name','table':'ar_freight_headers'},
'ArFreightLines':{'pk':'freight_line_id','uk':'freight_name','table':'ar_freight_lines'},
'ArInvoiceHeaders':{'pk':'invoice_header_id','uk':'invoice_number','table':'ar_invoice_headers'},
'ArOrderpadHeaders':{'pk':'orderpad_header_id','uk':'orderpad_name','table':'ar_orderpad_headers'},
'ArPaymentHeaders':{'pk':'payment_header_id','uk':'payment_number','table':'ar_payment_headers'},
'ArPaymentLines':{'pk':'payment_line_id','uk':'payment_header_id,invoice_header_id,pmnt_method_id',
                  'table':'ar_payment_lines'},
'ArSalcrGroups':{'pk':'salcr_group_id','uk':'salcr_group_name','table':'ar_salcr_groups'},
'ArSalesorderHeaders':{'pk':'order_header_id','uk':'order_number','table':'ar_salesorder_headers'},
'ArSalesPersons':{'pk':'sales_person_id','uk':'sales_person_number','table':'ar_sales_persons'},
'ArSoimportBatch':{'pk':'batch_id','uk':'batch_name','table':'ar_soimport_batch'},
'CmnBanks':{'pk':'bank_id','uk':'bank_name','table':'cmn_banks'},
'CmnBankAccounts':{'pk':'bank_account_id','uk':'branch_code,branch_acctnumber','table':'cmn_bank_accounts'},
'CmnBankCheques':{'pk':'bank_id,cba_bank_account_id,','uk':'cba_bank_account_id,cheque_no_from',
                  'table':'cmn_bank_cheques'},
'CmnCards':{'pk':'card_id','uk':'card_number','table':'cmn_cards'},
'CmnCardOptions':{'pk':'card_options_id','uk':'card_category_code','table':'cmn_card_options'},
'CmnCommodityCodes':{'pk':'ccc_id','uk':'commodity_code','table':'cmn_commodity_codes'},
'CmnContainers':{'pk':'pc_id','uk':'pc_name','table':'cmn_containers'},
'CmnCountries':{'pk':'country_code','uk':'country_name','table':'cmn_countries'},
'CmnFunctions':{'pk':'function_id','uk':'func_short_name','table':'cmn_functions'},
'CmnImportBatch':{'pk':'batch_id','uk':'batch_name','table':'cmn_import_batch'},
'CmnLookupLinks':{'pk':'cll_id','uk':'lookup_type,lookup_code,sl_no','table':'cmn_lookup_links'},
'CmnMenus':{'pk':'menu_id','uk':'parent_menu_id,menu_name','table':'cmn_menus'},
'CmnModules':{'pk':'module_id','uk':'module_name','table':'cmn_modules'},
'CmnObjectBatches':{'pk':'batch_id','uk':'source_object_name,name','table':'cmn_object_batches'},
'CmnObjectBatchLines':{'pk':'batch_line_id','uk':'source_object_name,source_object_id1,source_object_id2',
                       'table':'cmn_object_batch_lines'},
'CmnObjectStatuses':{'pk':'status_id','uk':'source_object_name,source_object_id1,source_object_id2',
                     'table':'cmn_object_statuses'},
'CmnParameters':{'pk':'parameter_id','uk':'name','table':'cmn_parameters'},
'CmnPaymenttermBreakups':{'pk':'cpb_id','uk':'cpb_name','table':'cmn_paymentterm_breakups'},
'CmnPaymentMethods':{'pk':'pmnt_method_id','uk':'pmnt_code','table':'cmn_payment_methods'},
'CmnPaymentTerms':{'pk':'cpt_id','uk':'terms_days','table':'cmn_payment_terms'},
'CmnPeriodBreakdowns':{'pk':'period_breakdown_id','uk':'period_header_id,period_line_id,sub_ledger_code,period_breakdown_category',
                       'table':'cmn_period_breakdowns'},
'CmnPeriodHeaders':{'pk':'period_header_id','uk':'period_header_name','table':'cmn_period_headers'},
'CmnPeriodLines':{'pk':'period_line_id','uk':'period_name','table':'cmn_period_lines'},
'CmnPrinters':{'pk':'printer_id','uk':'printer_name','table':'cmn_printers'},
'CmnPrivileges':{'pk':'privilege_id','uk':'name','table':'cmn_privileges'},
'CmnProfiles':{'pk':'profile_id','uk':'name','table':'cmn_profiles'},
'CmnProperties':{'pk':'property_id','uk':'object_id,property_name','table':'cmn_properties'},
'CmnPropertyObjects':{'pk':'object_id','uk':'object_name,object_value','table':'cmn_property_objects'},
'CmnPropertyValues':{'pk':'property_value_id','uk':'object_id,property_id,object_ref1,object_ref2,object_ref3',
                     'table':'cmn_property_values'},
'CmnReasons':{'pk':'reason_code_id','uk':'reason_name','table':'cmn_reasons'},
'CmnReportgroupHeaders':{'pk':'report_group_id','uk':'name','table':'cmn_reportgroup_headers'},
'CmnReportgroupLines':{'pk':'report_group_line_id','uk':'report_id,sl_no','table':'cmn_reportgroup_lines'},
'CmnReports':{'pk':'report_id','uk':'display_name','table':'cmn_reports'},
'CmnReportColumns':{'pk':'report_column_id','uk':'report_identifier','table':'cmn_report_columns'},
'CmnReportSet':{'pk':'set_id','uk':'parent_report_id,report_id','table':'cmn_report_set'},
'CmnResponsibilities':{'pk':'resp_id','uk':'resp_name','table':'cmn_responsibilities'},
'CmnSeasons':{'pk':'season_code_id','uk':'season_code','table':'cmn_seasons'},
'CmnSequences':{'pk':'cs_id','uk':'bu_id,seq_name','table':'cmn_sequences'},
'CmnStpAttributes':{'pk':'attribute_id','uk':'stp_id,attribute_code,attribute_value','table':'cmn_stp_attributes'},
'CmnStpLevels':{'pk':'level_id','uk':'stp_id,level_number,level_type,level_code','table':'cmn_stp_levels'},
'CmnStylePatterns':{'pk':'stp_id','uk':'stp_code','table':'cmn_style_patterns'},
'CmnTaxBreakups':{'pk':'ctb_id','uk':'ctb_name','table':'cmn_tax_breakups'},
'CmnTaxCodes':{'pk':'tax_code_id','uk':'tax_code','table':'cmn_tax_codes'},
'CmnTerminals':{'pk':'terminal_id','uk':'name','table':'cmn_terminals'},
'CmnTerminalProperties':{'pk':'terminal_property_id','uk':'terminal_id,name','table':'cmn_terminal_properties'},
'CmnUserExclusions':{'pk':'exclusion_id','uk':'user_id,function_id','table':'cmn_user_exclusions'},
'CmnUnitOfMeasurements':{'pk':'uom_id','uk':'uom_short_desc','table':'cmn_unit_of_measurements'},
'EmpDepartments':{'pk':'department_id','uk':'department_name','table':'emp_departments'},
'EmpJobs':{'pk':'job_id','uk':'job_name','table':'emp_jobs'},
'EmpJobTypes':{'pk':'job_type_id','uk':'job_type','table':'emp_job_types'},
'EmpPositions':{'pk':'position_id','uk':'position_name','table':'emp_positions'},
'EmpWorkingDays':{'pk':'working_day_id','uk':'working_day','table':'emp_working_days'},
'ExportHeaders':{'pk':'export_header_id','uk':'export_name','table':'export_headers'},
'GlAccountCodes':{'pk':'gl_account_id','uk':'gl_account_code','table':'gl_account_codes'},
'GlCashingupLines':{'pk':'cashingup_line_id','uk':'cashingup_id,transaction_source,transaction_source_id,transaction_payment_id',
                    'table':'gl_cashingup_lines'},
'GlJeHeaders':{'pk':'je_header_id','uk':'je_name','table':'gl_je_headers'},
'GlJeLines':{'pk':'je_lines_id','uk':'je_header_id,sl_no','table':'gl_je_lines'},
'GlTemplates':{'pk':'template_id','uk':'template_name','table':'gl_templates'},
'ImpexpHeaders':{'pk':'impexp_header_id','uk':'impexp_name','table':'impexp_headers'},
'ImpexpLines':{'pk':'impexp_line_id','uk':'impexp_header_id,sl_no','table':'impexp_lines'},
'InvBarcodeRepository':{'pk':'repository_id','uk':'barcode','table':'inv_barcode_repository'},
'InvBom':{'pk':'bom_id','uk':'parent_item_id,bom_level,item_id','table':'inv_bom'},
'InvBomTrans':{'pk':'bom_trans_id','uk':'transaction_source,transaction_header_id,transaction_line_id,item_id',
               'table':'inv_bom_trans'},
'InvContainerLog':{'pk':'container_log_id','uk':'container_number','table':'inv_container_log'},
'InvItemCategories':{'pk':'category_id','uk':'category_name','table':'inv_item_categories'},
'InvItemCountHeaders':{'pk':'item_count_header_id','uk':'batch_name','table':'inv_item_count_headers'},
'InvItemDimensions':{'pk':'dimension_id','uk':'item_id','table':'inv_item_dimensions'},
'InvItemDimensionLines':{'pk':'dimension_line_id','uk':'dimension_item_id,item_id','table':'inv_item_dimension_lines'},
'InvItemMasters':{'pk':'item_id','uk':'item_number','table':'inv_item_masters'},
'InvItemBarcodes':{'pk':'barcode_id','uk':'barcode','table':'inv_item_barcodes'},
'InvItemSalesUnits':{'pk':'su_id','uk':'su_number','table':'inv_item_sales_units'},
'InvItemMultiSeasons':{'pk':'multi_season_id','uk':'item_id,season_code_id','table':'inv_item_multi_seasons'},
'InvItemOfferHeaders':{'pk':'offer_header_id','uk':'group_code','table':'inv_item_offer_headers'},
'InvItemOfferLines':{'pk':'offer_line_id','uk':'group_code','table':'inv_item_offer_lines'},
'InvItemSerialNumbers':{'pk':'serial_number_id','uk':'iim_item_id,serial_number','table':'inv_item_serial_numbers'},
'InvItemSublocGroups':{'pk':'isg_id','uk':'location_id,item_id,sub_loc_group_code','table':'inv_item_subloc_groups'},
'InvItemSubCategories':{'pk':'sub_category_id','uk':'iic_category_id,sub_category_name',
                        'table':'inv_item_sub_categories'},
'InvLocations':{'pk':'location_id','uk':'location_name','table':'inv_locations'},
'InvLocationPricelists':{'pk':'location_pricelist_id','uk':'location_id,pricelist_header_id',
                         'table':'inv_location_pricelists'},
'InvManufacturers':{'pk':'manf_id','uk':'manf_name','table':'inv_manufacturers'},
'InvMkuptempHeaders':{'pk':'mkuptemp_id','uk':'mkuptemp_name','table':'inv_mkuptemp_headers'},
'InvMkuptempLines':{'pk':'mkuptemp_line_id','uk':'mkuptemp_id,price_type_id','table':'inv_mkuptemp_lines'},
'InvPallets':{'pk':'pallet_id','uk':'container_log_id,pallet_number','table':'inv_pallets'},
'InvPriceBreakHeaders':{'pk':'price_break_id','uk':'name','table':'inv_price_break_headers'},
'InvPriceBreakLines':{'pk':'price_break_line_id','uk':'ipbh_price_break_id,qty_from,qty_to',
                      'table':'inv_price_break_lines'},
'InvPriceTypes':{'pk':'price_type_id','uk':'price_type_name','table':'inv_price_types'},
'InvQuickcodeHeaders':{'pk':'quickcode_id','uk':'quickcode_name','table':'inv_quickcode_headers'},
'InvQuickcodeLines':{'pk':'quickcode_line_id','uk':'quickcode_id,item_id','table':'inv_quickcode_lines'},
'InvRequisitionHeaders':{'pk':'requisition_id','uk':'requisition_name','table':'inv_requisition_headers'},
'InvSimilarItemHeaders':{'pk':'similar_item_id','uk':'short_desc','table':'inv_similar_item_headers'},
'InvSlocassignHeaders':{'pk':'assignment_id','uk':'assignment_name','table':'inv_slocassign_headers'},
'InvStktakeItems':{'pk':'stktake_item_id','uk':'item_id,stktake_type_id','table':'inv_stktake_items'},
'InvStktakeTypes':{'pk':'stktake_type_id','uk':'stktake_name','table':'inv_stktake_types'},
'InvStocksplitHeaders':{'pk':'stocksplit_id','uk':'stocksplit_name','table':'inv_stocksplit_headers'},
'InvSublocHierarchy':{'pk':'hierarchy_id','uk':'location_id,sl_no','table':'inv_subloc_hierarchy'},
'InvSubLocations':{'pk':'sub_location_id','uk':'il_location_id,sub_location','table':'inv_sub_locations'},
'PalletBoxes':{'pk':'box_id','uk':'box_name','table':'pallet_boxes'},
'PalletHeaders':{'pk':'pallet_header_id','uk':'pallet_name','table':'pallet_headers'},
'PalletLines':{'pk':'pallet_line_id','uk':'pallet_header_id,box_id,sub_location_id,item_id','table':'pallet_lines'},
'PoBuyers':{'pk':'po_buyer_id','uk':'buyer_id,supervisor_id','table':'po_buyers'},
'PoOrderpadHeaders':{'pk':'orderpad_header_id','uk':'orderpad_name','table':'po_orderpad_headers'},
'PriceTemplateHeaders':{'pk':'pricetemp_id','uk':'pricetemp_name','table':'price_template_headers'},
'PriceTemplateLines':{'pk':'pricetemp_line_id','uk':'pricetemp_id,sales_unit','table':'price_template_lines'},
'PriceUpdateitemcpLines':{'pk':'updateitemcp_line_id','uk':'updateitemcp_line_id,item_id',
                          'table':'price_updateitemcp_lines'},
'PrPricelistHeaders':{'pk':'pricelist_header_id','uk':'pricelist_name','table':'pr_pricelist_headers'},
'SysControlHeaders':{'pk':'control_header_id','uk':'control_type,identifier','table':'sys_control_headers'},
'SysControlLines':{'pk':'control_line_id','uk':'control_header_id,control_line_type,identifier',
                   'table':'sys_control_lines'},
'SysNotificationEvents':{'pk':'event_id','uk':'identifier','table':'sys_notification_events'},
'SysPrograms':{'pk':'program_id','uk':'identifier','table':'sys_programs'},
'SysScheduleJobs':{'pk':'job_id','uk':'job_name','table':'sys_schedule_jobs'},
'SysUiitemattrs':{'pk':'item_attr_id','uk':'item_id,attribute_id','table':'sys_uiitemattrs'},
'SysUiitems':{'pk':'item_id','uk':'region_id,name','table':'sys_uiitems'},
'SysUiregions':{'pk':'region_id','uk':'name','table':'sys_uiregions'},
'TpStockSources':{'pk':'tp_source_id','uk':'tp_source_name','table':'tp_stock_sources'},
'TpStockLines':{'pk':'tp_stock_line_id','uk':'tp_uk','table':'tp_stock_lines'},
'WwwNodes':{'pk':'www_node_id','uk':'www_sub_source_id,source_node_id','table':'www_nodes'},
'WwwSources':{'pk':'www_source_id','uk':'www_source_name','table':'www_sources'},
'WwwSubSources':{'pk':'www_sub_source_id','uk':'www_source_id,sub_source_name','table':'www_sub_sources'},
}

def get_classname(p_table:str):
    return p_table.title().replace('_','')

def get_keybyTable(p_table,p_key = 'pk'):
    try:
        classname = get_classname(p_table)
        pk = PRIMARY_KEY[classname][p_key]
        return pk
    except Exception as ex:
        return None

def get_keybyClass(p_cls:str,p_key = 'pk'):
    pk = None
    try:
        pk = PRIMARY_KEY[p_cls][p_key]
        return pk
    except Exception as ex:
        print('get pk',ex)
        return None

def get_row_type(p_model):
    rowtype = {}
    try:
        for col in  p_model.__table__.columns:
            rowtype[col.name] = None
    except:
        pass
    finally:
        return rowtype

