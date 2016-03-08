# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose:  read items from  queue
# Author:
# Date: 2016-1-22
#-------------------------------------
import json

import pika

from conf.config import first_mongodb, redisdb


def resetRedis(mongodb):
    for item in mongodb.find():
        redisdb.sadd(item.itemid)
        
def receiveItemsFromQueue(rabbitmq_host="localhost"):
    
    queue = "insert_crawl_items"
    
    credentials = pika.PlainCredentials('root', 'root123')
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    
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
        resetRedis(mongodb)
        for item in items :
            if redisdb.sismember("smzdmfx_itemids", item.itemid):
                continue
            redisdb.sadd("smzdmfx_itemids", item.itemid)
            mongodb.insert(item)
            print "insert item %s successfully" %item['itemid']
        print "all items inserted"
        ch.basic_ack(delivery_tag = method.delivery_tag)
    
    # channel.basic_qos(prefetch_count=1)#同一时间点值处理一个message
    # channel.basic_consume(callback, queue='hello')
    channel.basic_consume(callback, queue=queue)
    channel.start_consuming()