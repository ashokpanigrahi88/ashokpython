import os
OUTBOUND_DIRECTORY=os.getenv('OUTBOUND_DIRECTORY','d:/oratech/outbound/')
DB_SERVER=os.getenv('DB_SERVER','-1')
DB_PORT=os.getenv('DB_PORT',1521)
DB_SID=os.getenv('DB_SID','-1')
DB_USERNAME=os.getenv('DB_USERNAME','-1')
DB_PASSWORD=os.getenv('DB_PASSWORD','-1')
DATA_FREQUENCY=os.getenv('DATA_FREQUENCY','3600' ) #every hour
QTYINSTOCK_FREQUENCY=os.getenv('QTYINSTOCK_FREQUENCY','300')  #every five minutes