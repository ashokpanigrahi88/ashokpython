import os

def setkey(p_key, p_val):
    if p_key not in os.environ:
        os.environ[p_key] = p_val

def getkey(p_key):
    return os.environ.get(p_key,'NOTDEFINED')


setkey("ORATECH_CANNON_PWD","ORATECHCANNON")
setkey("ORATECH_DATAHUB_PWD","ORATECHDATAHUB")
setkey("WHAT_WAREHOUSE_PWD","WHATWAREHOUSE")
setkey("WHAT_WAREHOUSELIVE_PWD","ORATECHLIVE")
setkey("ORATECH_CANNON_LIVE_PWD","ORATECHLIVE")
setkey("WHAT_NUEPOS_PWD","YFYnL63dhyfLeumv")
setkey("WHAT_NUEPOS_PWD","YFYnL63dhyfLeumv")
setkey("ORATECH_DATAHUB_FTPHOST","sftp.saasleaders.com")
setkey("ORATECH_DATAHUB_FTPUSER","saasleaders")
setkey("ORATECH_DATAHUB_FTPPWD","M@ngo$2021#")
setkey("ORATECH_DATAHUB_FTPPORT","21")

