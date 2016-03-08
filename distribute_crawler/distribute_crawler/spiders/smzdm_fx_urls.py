# -*- coding: UTF-8 -*-
'''
Created on 2016-1-22

@author: mushua
'''
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider

from conf.config import redisdb
from utils import receiveItemsFromQueue
from utils.net_util import loadHtmlSelector


class smzdmFx_urls_Spider(RedisSpider):
    '''
    Classdocs
    '''
    name = "GrabSmzdmfxUrls"
    allowed_domains=["faxian.smzdm.com"]
    start_urls=["http://faxian.smzdm.com/"]
    redis_key = "SmzdmfxUrls"
    
    
    def parse(self, response):
        print "parse"
        
        self.parseUrls()
        
        pass
    
    def parseUrls(self):
        
        print "parseUrls"
        
        source_url = "http://faxian.smzdm.com/"
        
        while 1 :
            
            selector = loadHtmlSelector(source_url, method="GET")
            
            if selector is None or selector.find("ul", {"class":"pagination"}): return
            if selector.find("ul", {"class":"pagination"}).find("li", {"class":"pagedown"}) is not None :
                link_next = selector.find("ul", {"class":"pagination"}).find("li", {"class":"pagedown"}).find("a").attrs['href']
#                 redisdb.rpushx("SmzdmfxUrls", link_next)
                redisdb.sadd("SmzdmfxUrls",link_next)
                source_url = link_next
                print source_url
#                 receiveItemsFromQueue()
            else :
                print "SmzdmfxUrls are all grabed" 
                return
                
#         while 1 :
#             receiveItemsFromQueue()
            
            
            