# encoding: utf-8
import os, sys, inspect
import agent_settings

sys.path.insert(0, agent_settings.common_modules_dir)
import frontpage.settings as settings
import frontpage.packageinfo as packageinfo
from frontpage.models import App
from django.db import connection as django_connection


import pika

sys.path.insert(0, settings.vuln_analysis_dir)
#import analyzeme

connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host, heartbeat_interval=10000))
channel = connection.channel()
channel.exchange_declare(exchange=agent_settings.marvin_exchange_pr, exchange_type = "direct")
channel.queue_declare(agent_settings.process_queue_vuln, durable = True)
channel.queue_bind(exchange = agent_settings.marvin_exchange_pr, 
                      queue = agent_settings.process_queue_vuln, 
                      routing_key = agent_settings.routing_key_vuln)

# out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))
# out_channel = out_connection.channel()
# out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_dyn, type = "direct")
# out_channel.queue_declare(agent_settings.process_queue_bayes,  durable = True)
# out_channel.queue_declare(agent_settings.process_queue_vuln,   durable = True)
# out_channel.queue_declare(agent_settings.process_queue_monkey, durable = True)
# out_channel.queue_bind(exchange = agent_settings.marvin_exchange_pr, 
#                        queue = agent_settings.process_queue_bayes, 
#                        routing_key = agent_settings.routing_key_bayes)
# out_channel.queue_bind(exchange = agent_settings.marvin_exchange_pr, 
#                        queue = agent_settings.process_queue_bayes, 
#                        routing_key = agent_settings.routing_key_new_file)

if sys.argv[1] == "dummy":
    dummy = True
else:
    dummy = False


def callback(ch, method, properties, body):
    if dummy:
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return
    print "[x] Mensaje recibido, buscar vulnerabilidades en %r" % (body,)
    django_connection.close()
    app_id = int(body)
    myApp = App.objects.get(pk=app_id)
    myApp.SAstatus = App.START_VF
    myApp.save()
    packageinfo.vuln_analysis_retry_worker(myApp)
    print "[x] %r escaneado por vulnerabilidades, actualizando... " % (app_id,)
    myApp = App.objects.get(pk=app_id)
    myApp.SAstatus = App.END_VF
    myApp.save()
    #marvin_es.update_apk(app_id, vuln_report)
    # out_channel.basic_publish(exchange = agent_settings.marvin_exchange_dyn, 
    #                           routing_key = agent_settings.routing_key_new_file,
    #                           body = filename,
    #                           properties = pika.BasicProperties(delivery_mode = 2))
    print "[x] %r actualizado\n" % (body,)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback, queue = agent_settings.process_queue_vuln)
channel.start_consuming()
