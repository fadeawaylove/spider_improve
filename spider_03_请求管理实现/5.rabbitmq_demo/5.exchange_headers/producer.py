import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

exchange_type = "headers_ex"
channel.exchange_declare(exchange=exchange_type,
                         exchange_type='headers')

headers = {
    "key1": "value1",
    "key2": "value2"
}

for i in range(10):
    message = "data%d"%i
    channel.basic_publish(exchange=exchange_type,
                          routing_key='',
                          body=message,
                          properties=pika.BasicProperties(headers = headers)
                          )
    print(" [x] Sent %r:%r" % (headers, message))

connection.close()

if __name__ == '__main__':
    pass