import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

exchange_name = "topic_ex"
channel.exchange_declare(exchange=exchange_name,
                         exchange_type='topic')


# a.b.c
routing_key = 'china.beijing.street'

for i in range(10):
    message = 'street-%d'%i
    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=message)

    print(" [x] Sent %r:%r" % (routing_key, message))

connection.close()

if __name__ == '__main__':
    pass