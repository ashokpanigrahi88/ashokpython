import os
Host="smtp.gmail.com"
Port="587"
Domain="oratechsolutions.biz"
Username=os.environ.setdefault("SMTP_USERNAME","unknown")
Password=os.environ.setdefault("SMTP_PASSWORD","unknown")
Ssl="YES"
Tls="NO"
Authenticate="YES"
From=Username
Outbounddir="y:/oratechjobs/"
Inbounddir="y:/oratechjobs/"
Faileddir="y:/oratechjobs/failed/"
Processingdir="y:/oratechjobs/processing/"
Processeddir="y:/oratechjobs/processed/"
Logdir="y:/oratechjobs/log/"
Fileprefix="otch_"
Fileextension="xml"
Signature="""Thanks
KD Wholesale Cash and Carry
"""
Serial="YES"
Tracelevel="0:None"
Mapdirectory="YES"
Mapdirectoryfrom="d:"
Mapdirectoryto="Y:"
