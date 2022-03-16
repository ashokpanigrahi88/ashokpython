import os
import time
import shutil
import glob
from jobhandler import db as db
import jobhandler.smtpclientinfo as config

def fileexists(p_filename):
    try:
        return os.path.exists(p_filename)
    except Exception as ex:
        print(ex)
        return True


def list_documentfile(p_module:str = 'INV',
                        p_daysfrom:int = 1,
                        p_daysto:int = 0,
                        p_customerid:int = None,
                        p_documentid:int = None,
                        p_sql:str = None,
                        p_hint:str = 'FILE',
                        p_action:str = 'NEW',
                        p_mapdrivefrom:str = None,
                        p_mapdriveto:str = None,
                        p_invoiceid:int = None
                ):
    v_reportname  = ""
    v_reportfile  = ""
    v_reporturl   = ""
    v_parameters  = ""
    v_sql	       = ""
    v_cur  	    = None
    v_documentnumber = ""
    v_customerid	= 0
    v_moduleid	 = ""
    v_invoicestatus = 'APPROVED'
    v_invoicetype = 'INVOICE'
    v_fileexists  = False
    v_msg          = ""
    v_invoiceid  = 0
    v_buid    = 1
    v_locationid    = 0
    v_email    = ""
    if p_module in ['INV','CRNOTE','DLNOTE']:
        if p_module == 'INV':
            v_invoicetype = 'INVOICE'
        else:
            p_module = 'CRNOTE'
            v_Invoicetype = 'CREDIT NOTE'

        v_sql =  """ Select c.Customer_ID ,c.Customer_Number  ,i.Invoice_Number,i.Invoice_Header_ID,
              Decode(i.Bu_ID,0,1,i.Bu_Id) bu_id ,
              Decode(nvl(i.Shipfrom_Location_ID,0),0,2,i.Shipfrom_Location_ID) location_id,c.Email,
              sysdate-i.Invoice_Status_Date
               From   Ar_Customers c, Ar_Invoice_Headers i
	       Where  c.Customer_ID  	= i.Customer_ID
               And    c.Customer_ID 	= nvl({},c.Customer_ID)
               And    i.Invoice_Header_ID = Nvl({},i.Invoice_Header_ID)
               And    i.Invoice_Status = '{}'
               And    i.Invoice_Type   = '{}'
               And    i.Invoice_Status_Date between  trunc(Sysdate) - {} and Trunc(Sysdate) - {}
               """.format('null','null',v_invoicestatus,v_invoicetype,p_daysfrom,p_daysto)
        print(v_sql)
        with  db.get_cursor() as cur:
            rows = cur.execute(v_sql)
            for row in rows:
                v_customerid = row[0]
                v_documentnumber = row[1]
                v_moduleid = row[2]
                v_invoiceid = row[3]
                v_buid = row[4]
                v_locationid = row[5]
                v_email = row[6]
                with db.get_cursor() as cur1:
                    v_reportfile = cur1.callfunc('AR_PKG.getdestination',str,
                                            keywordParameters = dict(p_id = v_customerid,
                                                                     p_destype = 'FILE',
                                                                     p_module = str(p_module),
                                                                     p_moduleid = str(v_moduleid)))
                v_mappedreportfile = v_reportfile.replace(config.Mapdirectoryfrom,config.Mapdirectoryto)
                v_fileexists = fileexists(v_mappedreportfile)
                print(v_customerid,v_documentnumber,v_moduleid, v_reportfile,v_mappedreportfile)
                if not v_fileexists:
                    # generate report file
                    if p_module in ['INV', 'CRNOTE']:
                        with db.get_cursor() as cur2:
                            v_msg = cur2.callfunc("Print_Pkg.Handle_Report", str,
                                                  keywordParameters = dict(
                                                    P_PrimaryParamName =  'P_SALESINVNUMBER',
                                                    p_PrimaryParamValue=  v_moduleid,
                                                    p_DocumentType =  'INV',
                                                    p_DesName =  v_reportfile,
                                                    p_Destype =  'FILE',
                                                    p_Report =  'SALESINVOICE',
                                                    p_ID =  v_customerid,
                                                    p_BuID =  v_buid,
                                                    p_LocationId =  v_locationid,
                                                   p_Schedule =  'YES',
                                                   p_Action =  'RECREATE'
                                                  ))
                            """
                            v_report = cur2.callfunc("SALORDER_PKG.defaultreport",str,['SALESINVOICE'])
                            print('PrintPkg:Building URL',v_report)
                            v_otherparams = "&P_SALESINVNUMBER={}".format(v_moduleid)
                            v_reporturl = cur2.callfunc("Utility_Pkg.BuildReportUrl",str,
                                                        keywordParameters = dict(
                                                        p_calltype = 'URL',
                                                        p_reportmode = 'ASYNCH',
                                                        p_reportname = v_report,
                                                        p_reporttype = '.rdf',
                                                        p_reporttitle = 'SALESINVOICE',
                                                        p_destype = 'FILE',
                                                        p_desformat = 'PDF',
                                                        p_buid = v_buid,
                                                        p_LocationID = v_locationid,
                                                        p_desname = v_reportfile,
                                                        p_OtherParams = v_otherparams
                                                         )
                                                         )
                            print(v_reporturl)
                            """
