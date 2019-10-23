import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

exchange_type = "headers_ex"
channel.exchange_declare(exchange=exchange_type,
                         exchange_type='headers')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# all表示所有的键值都必须一一匹配，才可以
# any表示任意一个键值匹配上，就可以
match_type = "any"
headers = {
    "x-match": match_type,   # 必须提供，
    'key1': 'value1',
    'key2': 'value3'
}

channel.queue_bind(exchange=exchange_type,
                   queue = queue_name,
                   arguments = headers)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r:%r" % (match_type, properties.headers, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

if __name__ == '__main__':
    pass