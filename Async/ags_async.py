from twisted.internet import defer, reactor
from twisted.web.client import getPage
import json

servers = ['host_name1:6080', 'host_name2:6080', 'host_name3:6080', 'host_name4:6080', 'host_name5:6080']
 
def listCallback(results):
    # return a property from each of the json responses
    soapUrls = map(lambda r: json.loads(r[1])['soapUrl'], results)
    print soapUrls

 
def finish(result):
    reactor.stop()
 

def test_site():
    # construct list of urls
    urls = map(lambda s: 'http://' + s + '/arcgis/rest/info?f=json', servers)

    deferreds = []

    # send all requests
    for url in urls:
        d = getPage(url)
        deferreds.append(d)

    # await all responses
    dl = defer.DeferredList(deferreds)
    dl.addCallback(listCallback)
    dl.addCallback(finish)

 
test_site()
reactor.run()