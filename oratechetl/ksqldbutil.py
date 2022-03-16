import logging
from ksql import KSQLAPI
from ksql import utils as ksqlutils
logging.basicConfig(level=logging.INFO)


KSQLHOST = "35.230.133.131"
KSQLPORT = '8088'
KSQLMETHOD = 'http://'
KSQLURL = "{}{}:{}".format(KSQLMETHOD,KSQLHOST,KSQLPORT)
KSQLKEY = ""
KSQLSECRET = ""

def ping_host(p_host=KSQLHOST, p_port=KSQLPORT):
    return ksqlutils.check_kafka_available("{}:{}".format(p_host,p_port))

class KSQLUtil:
    host = ""
    key = ""
    secret = ""
    http2 = False
    client = None
    def __init__(self,p_host, p_key="", p_secret="", p_http2=False):
        self.host = p_host
        self.key = p_key
        self.secret = p_secret
        self.http2 = p_http2
        self.connect()

    def connect(self):
        try:
            self.client = KSQLAPI(url=self.host, api_key=self.key, secret=self.secret)
        except Exception as ex:
            print(ex)
        finally:
            return self.client

    def show_streams(self):
        return ksqlutils.get_all_streams(self.client)

    def get_streaminfo(self,p_stream):
        return ksqlutils.get_stream_info(self.client,p_stream)
