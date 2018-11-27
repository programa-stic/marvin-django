# encoding: utf-8
#import inspect
import agent_settings
import os, sys
sys.path.insert(0, agent_settings.common_modules_dir)


import frontpage.settings as settings
import frontpage.packageinfo as packageinfo
import frontpage.classifier_interface_file as classifier_interface_file
import frontpage.apk_storage as apk_storage
from frontpage.models import App
from django.db import connection as django_connection
import pika
import logging

connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host, heartbeat_interval=10000))
channel = connection.channel()
channel.exchange_declare(exchange=agent_settings.marvin_exchange_andr, exchange_type = "direct")
channel.queue_declare(agent_settings.androlyze_queue, durable = True)
channel.queue_bind(exchange = agent_settings.marvin_exchange_andr, 
                      queue = agent_settings.androlyze_queue, 
                      routing_key = agent_settings.routing_key_andro)


if sys.argv[1] == "dummy":
    dummy = True
else:
    dummy = False

def callback(ch, method, properties, body):
  print "Dummy: " + repr(dummy)
  if dummy == False:
    print "[x] Mensaje recibido, analizar %r" % (body,)
    # django_connection.close()
    appId = int(body)
    # myApp = App.objects.get(pk=appId)
    myApp = App.objects.get(pk=appId)
    package_name = myApp.package_name
    md5 = myApp.md5
    try:
        rawfile = apk_storage.retrieve_apk(package_name, md5)
    except Exception as error:
        print "Error levantando archivo %r : %r " % (apk_storage.get_filepath(package_name, md5), repr(error))
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return
    print "[x] %r cargado" % (body)
    #fd = open(filename,'r')
    print "[x] Procesando %r" % (body)
    try:
      myApp.DCstatus = "In Progress"
      myApp.save()
      packageinfo.basic_analysis(rawfile, myApp)
      #packageinfo.decompile(myApp)
      #myApp = packageinfo.process_package(fd, None)
    except Exception as foo:
      print "Error procesando %r: " + repr(foo)
      return
    myApp = App.objects.get(pk=appId)
    myApp.DCstatus = "Complete"
    myApp.save()
    print "[x] %r procesado" % (body)
    django_connection.close()
    
    out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))
    out_channel = out_connection.channel()
    out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_pr, exchange_type = "direct")
    out_channel.queue_declare(agent_settings.process_queue_vuln,  durable = True)
    out_channel.queue_bind(exchange = agent_settings.marvin_exchange_pr, 
                           queue = agent_settings.process_queue_vuln, 
                           routing_key = agent_settings.routing_key_vuln)
    
    out_channel.basic_publish(exchange=agent_settings.marvin_exchange_pr,
                      routing_key = agent_settings.routing_key_vuln,
                      body = str(appId),
                      properties = pika.BasicProperties(delivery_mode = 2))
    ch.basic_ack(delivery_tag = method.delivery_tag)
  else:
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print "Package name: " + repr(body)

channel.basic_consume(callback, queue = agent_settings.androlyze_queue)
channel.start_consuming()
