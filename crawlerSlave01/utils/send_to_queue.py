# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose:  send items to master's queue
# Author:
# Date: 2016-1-22
#-------------------------------------

import json

import pika


def sendCrawlItemsToQueue(database, item_collection_name, items, rabbitmq_host="localhost"):
    if len(items) == 0 : return
    
    queue = "insert_crawl_items"
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue, durable=True)
    
    body_dic = {"database":database,
                "item_collection_name":item_collection_name,
                "items":items,
                }
    body = json.dumps(body_dic)
#     channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
    # message = ' '.join(sys.argv[1:]) or "hello world!"
    
    # channel.basic_publish(exchange='', routing_key='hello', body=message, 
    #                       properties=pika.BasicProperties(delivery_mode = 2,#make message persisitent
    #                     ))
    channel.basic_publish(exchange='', 
                          routing_key=queue, 
                          body=body,
                          properties=pika.BasicProperties(delivery_mode = 2,
                        ))
     
    print "[x] sent items" 
    
    connection.close()