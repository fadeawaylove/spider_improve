import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

exchange_name = "direct_ex"
channel.exchange_declare(exchange=exchange_name,
                         exchange_type='direct')

# 这里如果不写queue参数，那么意味着，由服务端随机产生一个队列
# 由于还加上了exclusive，所以这就实现了临时队列，连接已关闭，该随机队列也会被删除
# result = channel.queue_declare(exclusive=True)
# queue_name = result.method.queue

queue = "new_queue"
channel.queue_declare(queue=queue)

# 指当前队列要接受routing_key指为debug、info或warning的消息
binding_keys = ["debug", "test.info", "warning", "str"]

for binding_key in binding_keys:
    channel.queue_bind(exchange=exchange_name,
                       queue=queue,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue,
                      no_ack=True)

channel.start_consuming()

if __name__ == '__main__':
    pass