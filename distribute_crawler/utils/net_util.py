# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose:  spider load net
# Author:
# Date: 2015-10-28
#-------------------------------------
from _random import Random
import random

from bs4 import BeautifulSoup
import httplib2

from conf.config import redisdb


def loadHtmlSelector(url, method="GET", headers=None, contenttype='application/x-www-form-urlencoded', cookie='', openProxy=False):
    
    print "loadHtmlSelector"
    
    useragents = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                  "Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0"
                  ]
#     useragent = useragents[random.randint(0, len(useragents)-1)]
    useragent = useragents[0]
    
    if headers is None:
        headers = {"User-Agent":useragent, "content-type":contenttype, "Cookie":cookie}
    
    if openProxy :
        response, content = loadHtmlProxy(url, method="GET", headers=None, contenttype='application/x-www-form-urlencoded', cookie='')
        pass
    else :
        response, content = loadHtmlNoproxy(url, method="GET", headers=headers, contenttype='application/x-www-form-urlencoded', cookie='')
        
    return BeautifulSoup(content)
#     try :
#         h = httplib2.Http()
#         response, content = h.request(url, method="GET", headers=headers)
#         print str(response.status)
#         return BeautifulSoup(content)
#     
#     except Exception,e :
#         print repr(e)
        
      
def loadHtmlNoproxy(url, method="GET", headers=None, contenttype='application/x-www-form-urlencoded', cookie=''):
    print "loadHtmlNoproxy"
    
    try :
        h = httplib2.Http()
        response, content = h.request(url, method="GET", headers=headers)
        print str(response.status)
        return response, content
    
    except Exception,e :
        print repr(e)
    

def loadHtmlProxy(url, method="GET", headers=None, contenttype='application/x-www-form-urlencoded', cookie=''):
    print "loadHtmlProxy"
    
    #从redisdb获取免费代理
    proxys = redisdb.hkeys("proxys_free")
    if len(proxys) == 0 :
        print "proxys is none"
        return
    proxy = proxys[random.randint(0, len(proxys)-1)]
    ip = str(proxy).split(':')[0]
    port = str(proxy).split(':')[1]
    
    try :
        h = httplib2.HTTPConnectionWithTimeout(ip, port, timeout=6)
        h.request(url, method="GET", headers=headers)
        response = h.getresponse()
        print str(response.status)
        content = response.read()
        
    except Exception,e :
        print repr(e)
        
    finally :
        if h :
            h.close()
    
    return response, content
        
    
    
    
    
         