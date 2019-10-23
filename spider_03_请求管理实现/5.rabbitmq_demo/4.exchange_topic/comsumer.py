import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

exchange_name = "topic_ex"
channel.exchange_declare(exchange=exchange_name,
                         exchange_type='topic',)

result = channel.queue_declare(durable=True)
queue_name = result.method.queue

# *号匹配任意一个单词；#号匹配0个或多个单词
# china.a.b.c
# a.street
binding_keys = ['*.street', "china.#"]


for binding_key in binding_keys:
    channel.queue_bind(exchange=exchange_name,
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

if __name__ == '__main__':
    pass