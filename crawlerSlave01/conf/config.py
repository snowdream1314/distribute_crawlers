# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose: define database server
# Author:
# Date: 2016-1-22
#-------------------------------------

import pymongo
import redis

from crawlerSlave01.settings import REDIS_HOST, REDIS_PORT


redisdb = redis.Redis(host = REDIS_HOST, port = REDIS_PORT, db=0)

first_mongodb_domain = "localhost"
first_mongodb_port = 27017
first_mongodb = pymongo.MongoClient(first_mongodb_domain, first_mongodb_port)
