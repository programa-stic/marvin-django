# queue_handler.py
# Este programa envia pedidos de procesamiento en vez de hacerlo todo desde la UI

import settings
import sys
import pika
import simplejson

sys.path.insert(0, settings.agent_dir)
import agent_settings
from androguard.misc import AnalyzeAPK
from androlyze import APK
import frontpage.apk_storage as apk_storage
from frontpage.apk_storage import store_apk
from models import App, App_metadata
from hashlib import sha1, md5
import logging

out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))

out_channel = out_connection.channel()

out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_dl, exchange_type = "direct")

out_channel.queue_declare(agent_settings.download_queue, durable = True)

out_channel.queue_bind(exchange    = agent_settings.marvin_exchange_dl,
					   queue       = agent_settings.download_queue,
					   routing_key = agent_settings.routing_key_dl)

def flush_queue():
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))
		ch = connection.channel()

		response = ch.queue_purge(queue=agent_settings.download_queue)
		# import pdb; pdb.set_trace()
		if pika.spec.Queue.PurgeOk == type(response.method):
			print "Se vaciaron ", response.method.message_count, " mensajes de " + agent_settings.download_queue

		response = ch.queue_purge(queue=agent_settings.androlyze_queue)
		if pika.spec.Queue.PurgeOk == type(response.method):
			print "Se vaciaron ", response.method.message_count, " mensajes de " + agent_settings.androlyze_queue
		
		response = ch.queue_purge(queue=agent_settings.process_queue_vuln)
		if pika.spec.Queue.PurgeOk == type(response.method):
			print "Se vaciaron ", response.method.message_count, " mensajes de " + agent_settings.process_queue_vuln
		
		connection.close()

	except Exception as e:
		logging.error("Error vaciando agentes: " + repr(e) + "\n")
	
def queue_for_dl(package_name, app_md):
	
	myApp = App(package_name = package_name,
				app_name= app_md['title'],
				version = app_md['versionString'],
				DLstatus = App.QUEUED_STATUS)
	myApp.save()
	metadata = App_metadata(app_name= app_md['title'],
						version_string = app_md['versionString'],
						author = app_md['author'],
						date_upload = app_md['uploadDate'],
						description = app_md['description'],
						app = myApp)
	metadata.save()
	message = marshal_name_version(package_name, metadata.version_string)
	
	out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))
	
	out_channel = out_connection.channel()
	
	out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_dl, exchange_type = "direct")
	
	out_channel.queue_declare(agent_settings.download_queue, durable = True)
	
	out_channel.queue_bind(exchange    = agent_settings.marvin_exchange_dl,
						   queue       = agent_settings.download_queue,
						   routing_key = agent_settings.routing_key_dl)
	
	out_channel.basic_publish(exchange=agent_settings.marvin_exchange_dl, 
                      routing_key=agent_settings.routing_key_dl, 
	                  body = message, 
	                  properties = pika.BasicProperties(delivery_mode = 2), 
	                  mandatory = 1)

def queue_for_androlyze(myfile):
	rawfile = myfile.read()
	apk = APK(myfile.temporary_file_path())
	package_name = apk.get_package()
	md5hash = md5(rawfile).digest().encode('hex')
	sha1hash = sha1(rawfile).hexdigest()
	
	myApp = App(package_name = package_name,
				app_name= apk.get_app_name(),
				version = apk.get_androidversion_code(),
				DLstatus = App.DOWNLOADED)
	myApp.save()

	# metadata = App_metadata(app_name= app_md['title'],
	# 					version_string = app_md['versionString'],
	# 					author = app_md['author'],
	# 					date_upload = app_md['uploadDate'],
	# 					description = app_md['description'],
	# 					app = myApp)
	
	filename = store_apk(rawfile, package_name, md5hash)
	print "[x] %r almacenado en %r \n" % (package_name, filename)  
	myApp.md5 = md5hash
	myApp.sha1 = sha1hash
	myApp.save()

	params =  pika.ConnectionParameters(host=agent_settings.queue_host)

	out_connection = pika.BlockingConnection(params)

	out_channel = out_connection.channel()
	
	out_channel.exchange_declare(exchange=agent_settings.marvin_exchange_andr, exchange_type = "direct")
	
	out_channel.queue_declare(agent_settings.androlyze_queue, durable = True)
	
	out_channel.queue_bind(exchange    = agent_settings.marvin_exchange_andr,
	                   queue       = agent_settings.androlyze_queue,
	                   routing_key = agent_settings.routing_key_andro)
	
	out_channel.basic_publish(exchange = agent_settings.marvin_exchange_andr, 
	                      routing_key = agent_settings.routing_key_andro,
	                      body = (str(myApp.id)),
	                      properties = pika.BasicProperties(delivery_mode = 2),
	                      mandatory = 1)
	# out_connection.close()


def marshal_name_version(package_name, version_string):
	myDict = {'package_name':package_name,
			  'version_string': version_string}
	return simplejson.dumps(myDict)

def unmarshal_name_version(jsonString):
	myDict = simplejson.loads(jsonString)
	package_name = myDict['package_name']
	version_string = myDict['version_string']
	return (package_name, version_string)


