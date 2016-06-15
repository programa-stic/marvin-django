# queue_handler.py
# Este programa envia pedidos de procesamiento en vez de hacerlo todo desde la UI

import settings
import sys
import pika
import simplejson

sys.path.insert(0, settings.agent_dir)
import agent_settings
from models import App, App_metadata

out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))
out_channel = out_connection.channel()
out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_dl, type = "direct")
out_channel.queue_declare(agent_settings.download_queue, durable = True)
out_channel.queue_bind(exchange    = agent_settings.marvin_exchange_dl,
					   queue       = agent_settings.download_queue,
					   routing_key = agent_settings.routing_key_dl)


def queue_for_dl(package_name, app_md):

	myApp = App(package_name = package_name,
				app_name= app_md.docV2.title,
				version = app_md.docV2.details.appDetails.versionString,
				DLstatus = App.QUEUED_STATUS)
	myApp.save()
	metadata = App_metadata(app_name= app_md.docV2.title,
						version_string = app_md.docV2.details.appDetails.versionString,
						author = app_md.docV2.creator,
						date_upload = app_md.docV2.details.appDetails.uploadDate,
						description = app_md.docV2.descriptionHtml,
						app = myApp)
	metadata.save()
	message = marshal_name_version(package_name, metadata.version_string)
	out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))
	out_channel = out_connection.channel()
	out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_dl, type = "direct")
	out_channel.queue_declare(agent_settings.download_queue, durable = True)
	out_channel.queue_bind(exchange    = agent_settings.marvin_exchange_dl,
						   queue       = agent_settings.download_queue,
						   routing_key = agent_settings.routing_key_dl)
	out_channel.basic_publish(exchange=agent_settings.marvin_exchange_dl, 
                      routing_key=agent_settings.routing_key_dl, 
	                  body = message, 
	                  properties = pika.BasicProperties(delivery_mode = 2), 
	                  mandatory = 1)

def marshal_name_version (package_name, version_string):
	myDict = {'package_name':package_name,
			  'version_string': version_string}
	return simplejson.dumps(myDict)

def unmarshal_name_version(jsonString):
	myDict = simplejson.loads(jsonString)
	package_name = myDict['package_name']
	version_string = myDict['version_string']
	return (package_name, version_string)


