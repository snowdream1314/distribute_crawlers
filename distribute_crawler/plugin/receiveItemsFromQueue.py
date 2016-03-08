# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose:  read items from  queue
# Author:
# Date: 2016-1-22
#-------------------------------------
import json

import pika
import pymongo
import redis


# import sys
# sys.path.append(object)
# from conf.config import first_mongodb
first_mongodb_domain = "localhost"
first_mongodb_port = 27017
first_mongodb = pymongo.MongoClient(first_mongodb_domain, first_mongodb_port)

redisdb = redis.Redis(host="localhost", port=6379, db=0)

def resetRedis(mongodb):
    print "resetRedis"
    for item in mongodb.find():
        print item['itemid']
        print item
        redisdb.sadd("smzdmfx_items", item['itemid'])
        
queue = "insert_crawl_items"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue=queue, durable=True)

#     channel.exchange_declare(exchange='direct_logs', type='direct')

def callback(ch, method, properties, body):
    print "[x] received items"
    content = json.loads(body)
    database = content['database']
    item_collection_name = content['item_collection_name']
    items = content['items']
    if len(items) == 0 : return
    mongodb = first_mongodb[database][item_collection_name]
#     resetRedis(mongodb)
    for item in items :
        if redisdb.sismember("smzdmfx_items", item['itemid']):
            print  "%s already exits,drop" % item['itemid']
            continue
        redisdb.sadd("smzdmfx_items", item['itemid'])
        mongodb.insert(item)
        print "insert item %s successfully" %item['itemid']
    print "all items inserted"
    ch.basic_ack(delivery_tag = method.delivery_tag)

# channel.basic_qos(prefetch_count=1)#ͬһʱ���ֵ����һ��message
# channel.basic_consume(callback, queue='hello')
channel.basic_consume(callback, queue=queue)
channel.start_consuming()

        
        