# -*- coding: UTF-8 -*-
'''
Created on 2016-1-22

@author: mushua
'''
import datetime
import re
import time

from scrapy.spiders import Spider

from conf.config import redisdb
from items.item import Item
from utils.net_util import loadHtmlSelector
from utils.send_to_queue import sendCrawlItemsToQueue


class smzdmFx_urls_Spider(Spider):
    '''
    Classdocs
    '''
    name = "GrabSmzdmfxSlave01"
    allowed_domains=["faxian.smzdm.com"]
    start_urls=["http://faxian.smzdm.com/"]
#     redis_key = "SmzdmfxUrls"
    database = "smzdm_test"
    item_collection_name = "smzdm_fx_item_list"
    
    def parse(self, response):
        print "parse"
        
        self.parseItems()
        
        pass
    
    def parseItems(self):
        
        print "parseItems"
        
        
        while 1 :
            
            source_url = redisdb.rpop("SmzdmfxUrls")
            print source_url
            
            selector = loadHtmlSelector(source_url, method="GET")
            
            if selector is None : return

            lists = selector.findAll("li", {"class":"list"})
#             print divs
            item_list = []
            for list in lists :
                
                item = Item()
#                 item.categoryid = source['item_id']      #分类ID  
                
                #条目ID
                item.itemid = int (list.attrs['articleid'].split("_")[-1])
#                 clr.print_blue_text(item.itemid)
                print item.itemid
                
                #更新，直接跳到下�?个分�?
#                 num = mongodbItem.find({"itemid":item.itemid}).count()
#                 if num != 0 : return    
#                 if num != 0 : 
#                     clr.print_yellow_text("item exits")
#                     continue  #暂停，继续爬�?
                
                #时间  
                item.updatetime = int (list.attrs['timesort'])
                updatetime = time.asctime(time.localtime(item.updatetime))
                article_time = datetime.datetime.strptime(updatetime,"%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d %H:%M:%S %A")
                print item.updatetime
                print article_time
                
                #条目名称  
                item.name = list.find("h2", {"class":"itemName"}).find("span", {"class":"black"}).get_text().strip()
#                 print item.name
                  
                if "优惠券".decode('utf-8') in item.name : continue    #过滤非商品条目
                if "活动".decode('utf-8') in item.name : continue
                if "专享".decode('utf-8') in item.name : continue
                  
                #商品图片  
                item.image = list.find("img", alt=True)     
                if item.image :
                    item.image = item.image.attrs['src']
                    print item.image
                else :
                    item.image = ""
                
                    continue
                #价格  
                item.price = list.find("h2", {"class":"itemName"}).find("span", {"class":"red"}).get_text()     
#                 if item.price == '' : continue 
                if "促销".decode('utf-8') in item.price : continue
                if "红包".decode('utf-8') in item.price : continue    #过滤非商品条�?
                if  item.price != '' and not re.search(r'\d', item.price) : continue        #过滤价格中没有数字的条目
#                 print item.price
                
                #购买链接  
                item.href = list.find("div", {"class":"item_buy_mall"}).find("a", {"class":"directLink"}).attrs['href']
#                 clr.print_blue_text(item.href)     
#                 print item.href
                
                #推荐�?  
                goodcount = list.find("div", {"class":"zan_fav_com"}).find("a", {"class":"zan"}).find("em").get_text()      #“�?��?�数
                goodcountnum = int(goodcount)
                print "goodcountnum is %d" %goodcountnum        
                
                #评论�?  
                commentcount = list.find("div", {"class":"zan_fav_com"}).find("a", {"class":"comment"}).get_text()      
                commentcountnum = int(commentcount)
                print "commentcountnum is %d" %commentcountnum
                
                #文章链接
                article_url =  list.find("h2", {"class":"itemName"}).find("a").attrs['href']  
#                 print article_url
#                 clr.print_blue_text(article_url)
                
                article_selector = loadHtmlSelector(article_url, headers=None)
                
                #商城
                originmall = article_selector.find("div", {"class":"article-meta-box"}).find("a", {"onclick":None})
                if originmall :
                    originmall = originmall.get_text()
                else :
                    originmall = ""
#                 print originmall
                
#                 content_item = article_selector.find("article", {"class":"article-details"}).find("div", {"class":"item-box"})
#                 if content_item :
                #优惠力度
                youhui_content = article_selector.find("div", {"class":"item-box item-preferential"})
                if youhui_content :
                    youhui_content = youhui_content.find("div", {"class":"inner-block"})
                    if youhui_content :
                        youhui_content = youhui_content.find("p").get_text().replace("\t","").replace("\n", "").replace("\r", "").strip()
                    else :
                        youhui_content = ""
                    #爆料原文
                    baoliao_content = article_selector.find("div", {"class":"item-box item-preferential"}).find("div", {"class":"baoliao-block"})
                    if baoliao_content :
                        baoliao_content = baoliao_content.find("p").get_text().replace("\t","").replace("\n", "").replace("\r", "").strip()
                    else :
                        baoliao_content = ""
                else :
                    youhui_content = article_selector.find("article", {"class":"article-details"}).find("div", {"class":"inner-block"}).get_text().replace("\t","").replace("\n", "").replace("\r", "").strip()
                    baoliao_content = ""
#                 print youhui_content
#                 print baoliao_content
                
                #商品介绍
                item_description = ""
                item_descriptions = article_selector.findAll("div", {"class":"item-box"})
                if item_descriptions :
                    description_count = 1
                    for description in item_descriptions :
                        if description_count == 2 :
                            item_description = description.find("div", {"class":"inner-block"})
                            if item_description :
                                item_description = item_description.find("p")
                                if item_description :
                                    item_description = item_description.get_text().replace("\t","").replace("\n", "").replace("\r", "").strip()
                                else :
                                    item_description = ""
                            else :
                                    item_description = ""
                        description_count += 1
#                 print item_description
#                 else :
#                     baoliao_content = article_selector.find("article", {"class":"article-details"}).find("div", {"class":"inner-block"}).find("p", {"itemprop":"description"}).get_text().replace("\t","").replace("\n", "").replace("\r", "").strip()
#                     youhui_content = ""
#                     item_description = ""
                    
                #不推荐数
                badcount = article_selector.find("div", {"class":"score_rate"}).find("span", {"id":"rating_unworthy_num"}).get_text().strip()
                badcountnum = int(badcount)
                print "badcountnum is %d" %badcountnum
                
                #收藏�?
                favcount = article_selector.find("div", {"class":"operate_box"}).find("div", {"class":"operate_icon"}).find("a", {"class":"fav"}).find("em").get_text()
                favcountnum = int(favcount)
                print favcountnum 
                  
                item_dict = item.createItemdic({"originmall":originmall, "baoliao_content":baoliao_content, "youhui_content":youhui_content, "item_description":item_description, "bad_count":badcountnum, "fav_count":favcountnum, "article_url":article_url, "article_time":article_time, "good_count":goodcountnum, "comment_count":commentcountnum})
                print item_dict 
                
                item_list.append(item_dict)
            
            sendCrawlItemsToQueue(self.database, self.item_collection_name, item_list)
            
            
            
            
            
            
            