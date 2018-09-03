import pika
import agent_settings
import sys

fase = int(sys.argv[1])

print "Fase: %r" % fase

if fase == 1:
    exchange = agent_settings.marvin_exchange_dl
    queue = agent_settings.download_queue
    routing_key = agent_settings.routing_key_dl
elif fase == 2:
    exchange = agent_settings.marvin_exchange_andr
    queue = agent_settings.androlyze_queue
    routing_key = agent_settings.routing_key_andro
elif fase == 3:
    exchange = agent_settings.marvin_exchange_pr
    queue = agent_settings.process_queue_bayes
    routing_key = agent_settings.routing_key_new_file
elif fase == 4:
    exchange = agent_settings.marvin_exchange_pr
    queue = agent_settings.process_queue_bayes
    routing_key = agent_settings.routing_key_bayes
elif fase == 5:
    exchange = agent_settings.marvin_exchange_pr
    queue = agent_settings.process_queue_vuln
    routing_key = agent_settings.routing_key_vuln
elif fase == 6:
    exchange = agent_settings.marvin_exchange_pr
    queue = agent_settings.process_queue_monkey
    routing_key = agent_settings.routing_key_monkey

out_connection = pika.BlockingConnection(pika.ConnectionParameters(host=agent_settings.queue_host))
out_channel = out_connection.channel()
out_channel.exchange_declare(exchange=exchange, exchange_type = "direct")
out_channel.queue_declare(queue, durable = True)
out_channel.queue_bind(exchange=exchange,
	                   queue=queue,
	                   routing_key=routing_key)

message = sys.argv[2]
out_channel.basic_publish(exchange=exchange, 
                      routing_key=routing_key, 
	                  body = message, properties = pika.BasicProperties(
                      delivery_mode = 2), mandatory = 1)
print ("Sent for %r" % message)
out_connection.close()


