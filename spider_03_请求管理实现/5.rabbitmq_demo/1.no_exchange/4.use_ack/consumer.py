import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.211.55.3'))
channel = connection.channel()

queue_name = "queue"
channel.queue_declare(queue=queue_name)

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(1)
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=10)    # 指定服务端一次性发出多少条数据给消费者
channel.basic_consume(callback,
                      queue=queue_name)

channel.start_consuming()
if __name__ == '__main__':
    pass
