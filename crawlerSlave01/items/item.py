# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose:  spider item
# Author:
# Date: 2016-1-22
#-------------------------------------

import time


# from scrapy.item import Item, Field
class Item:
    
    itemid = None
    categoryid = 0
    name = None
    image = None
    href = ""
    brandname = ""
    price = None
    originprice = None
    updatetime = None
    
    def createItemdic(self,dict2):
        
        if dict2 == None :
            dict2 = {}
            
        if self.itemid  is None or self.name is None or self.price is None :
            print "params have Null"
            return None
         
        if not self.originprice :
            self.originprice = 0
            
        if not self.updatetime :
            self.updatetime = int (time.time())
            
        dict1 = {"itemid":self.itemid,"categoryid":self.categoryid,"name":self.name,"image":self.image,"href":self.href,"brandname":self.brandname,"price":self.price,"originprice":self.originprice,"updatetime":self.updatetime}
        return dict(dict2, **dict1)