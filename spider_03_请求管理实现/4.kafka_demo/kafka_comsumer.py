from confluent_kafka import Consumer, KafkaError, TopicPartition


c = Consumer({
    'bootstrap.servers': '10.211.55.3:29092',
    'group.id': 'mygroup2',
    'default.topic.config': {
        'auto.offset.reset': 'smallest'   # largest
    }
})

# tp = TopicPartition("mytopic", 2, 0)
# c.assign([tp])
# c.seek(tp)

c.subscribe(['mytopic'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    print('Received message: {} {} {}'.format(msg.value().decode('utf-8'), msg.topic(), msg.partition()))

c.close()


if __name__ == '__main__':
    pass