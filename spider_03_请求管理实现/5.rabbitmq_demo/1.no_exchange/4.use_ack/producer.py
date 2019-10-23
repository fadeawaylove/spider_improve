import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

queue_name = 'queue'
channel.queue_declare(queue=queue_name)

for i in range(100):
    message = "data%d"%i

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message)
    print(" [x] Sent %r" % message)

connection.close()

if __name__ == '__main__':
    pass