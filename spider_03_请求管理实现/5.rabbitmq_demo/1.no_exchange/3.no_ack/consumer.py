import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

queue_name = "queue"
channel.queue_declare(queue=queue_name)


print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    import time
    time.sleep(1)
    print(" [x] Done")

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=False)

channel.start_consuming()


if __name__ == '__main__':
    pass
