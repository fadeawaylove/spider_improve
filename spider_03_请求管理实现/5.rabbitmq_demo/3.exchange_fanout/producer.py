import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

exchange_name = "fanout_ex"
channel.exchange_declare(exchange=exchange_name,
                         exchange_type='fanout')

for i in range(10):
    message = "data%d"%i
    channel.basic_publish(exchange=exchange_name,
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % message)

connection.close()

if __name__ == '__main__':
    pass