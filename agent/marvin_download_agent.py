# encoding: utf-8
import os, sys, inspect
import agent_settings

sys.path.insert(0, agent_settings.common_modules_dir)

import settings
from djgpa.api import GooglePlay
import tempfile
from frontpage.packageinfo import process_package
from frontpage.models import App
from frontpage.queue_handler import unmarshal_name_version
from frontpage.apk_storage import store_apk
from django.db import connection


import pika
import logging
from hashlib import sha1, md5


if sys.argv[1] == "dummy":
    dummy = True
else:
    dummy = False


in_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))
in_channel = in_connection.channel()
in_channel.exchange_declare(exchange=agent_settings.marvin_exchange_dl, type = "direct")
in_channel.queue_declare(agent_settings.download_queue, durable=True)
in_channel.queue_bind(exchange = agent_settings.marvin_exchange_dl, 
	                  queue = agent_settings.download_queue, 
	                  routing_key = agent_settings.routing_key_dl)

# out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host,heartbeat_interval=10))
# out_channel = out_connection.channel()
# out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_andr, type = "direct")
# out_channel.queue_declare(agent_settings.androlyze_queue, durable = True)
# out_channel.queue_bind(exchange    = agent_settings.marvin_exchange_andr,
# 					   queue       = agent_settings.androlyze_queue,
# 					   routing_key = agent_settings.routing_key_andro)

def callback(ch, method, properties, body):
    if dummy == False:
        api = GooglePlay().auth()
        (package_name, version_string) = unmarshal_name_version(body)
        print "[x] Mensaje recibido, descargar %r" % (package_name)
        myApp = App.objects.filter(package_name=package_name, version=version_string)[0]
        myApp.DLstatus = App.DOWNLOADING
        myApp.save()
        print "[x] Not dummy, descargar %r" % (package_name)
        # matches = api.search_app(package_name)
        # print "[x] Encontre %r" % (matches)

        # if len(matches) == 0:
        #     print " [E] %r no coincide con ningún paquete de la Play Store" % (package_name,)
        #     ch.basic_ack(delivery_tag = method.delivery_tag)
        #     return
        # else:
        print "[x] descargando %r" % (package_name)
        myFile = tempfile.NamedTemporaryFile(delete=False)
        success = api.download(package_name, myFile.name)
        if success:
            print "[x] %r descargado " % (package_name)
            #details = api.details(body)
            myFile.seek(0)
            rawfile = myFile.read()
            md5hash = md5(rawfile).digest().encode('hex')
            sha1hash = sha1(rawfile).hexdigest()
            filename = store_apk(rawfile, package_name, md5hash)
            print "[x] %r almacenado en %r \n" % (package_name, filename)  
            myApp.md5 = md5hash
            myApp.sha1 = sha1hash
            myApp.DLstatus = App.DOWNLOADED
            myApp.save()
            connection.close()
            ch.basic_ack(delivery_tag = method.delivery_tag)
            # try:
            #     out_channel.basic_publish(exchange = agent_settings.marvin_exchange_andr, 
            #                               routing_key = agent_settings.routing_key_andro,
            #                               body = (str(myApp.id)),
            #                               properties = pika.BasicProperties(delivery_mode = 2))
            # except Exception as poof:
            #     logging.error ("Exception publishing to androlyze_queue: " + repr (poof))
                #out_connection.connect()
            out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host, heartbeat_interval=10))
            out_channel = out_connection.channel()
            out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_andr, type = "direct")
            out_channel.queue_declare(agent_settings.androlyze_queue, durable = True)
            out_channel.queue_bind(exchange    = agent_settings.marvin_exchange_andr,
                                   queue       = agent_settings.androlyze_queue,
                                   routing_key = agent_settings.routing_key_andro)
            out_channel.basic_publish(exchange = agent_settings.marvin_exchange_andr, 
                                      routing_key = agent_settings.routing_key_andro,
                                      body = (str(myApp.id)),
                                      properties = pika.BasicProperties(delivery_mode = 2))                
        else:
            print "[x] Error: Paquete %r no encontrado" % (package_name)
            ch.basic_ack(delivery_tag = method.delivery_tag)    
    else:
        print "Dummy, dumping message: %r" % body
        ch.basic_ack(delivery_tag = method.delivery_tag)
    #connection.close()
    #ch.basic_ack(delivery_tag = method.delivery_tag)


#api = GooglePlay().auth()
in_channel.basic_consume(callback, queue=agent_settings.download_queue)
in_channel.start_consuming()
