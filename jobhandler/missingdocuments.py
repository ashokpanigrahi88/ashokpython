from datetime import datetime
import time
from jobhandler import customerpkg
while True:
    print(datetime.now())
    customerpkg.list_documentfile(p_daysfrom=1,p_daysto=0)
    print('Gone to sleep for an hour')
    time.sleep(60*60)

