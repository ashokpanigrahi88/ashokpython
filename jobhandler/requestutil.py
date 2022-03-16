import requests
def unescape(p_url):
    p_url = p_url.replace("&lt;", "<")
    p_url = p_url.replace("&gt;", ">")
    # this has to be last:
    p_url = p_url.replace("&amp;", "&")
    return p_url
def runreport(p_url):
    reporturl = unescape(p_url)
    r =requests.get(reporturl)
    print(r.status_code)
    print(r.headers)