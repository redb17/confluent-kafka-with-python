from confluent_kafka import SerializingProducer
import json
from threading import Thread
import socket


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")

def serialize_json(obj, ctx):
    return json.dumps(obj).encode('utf-8')

def kafka_producer(broker):
    conf = {
        'bootstrap.servers': broker,
        'key.serializer': serialize_json,
        'value.serializer': serialize_json,
        'queue.buffering.max.messages': 1_000_000,
        'queue.buffering.max.kbytes': str(64 * 1024),
        'linger.ms': '300',
        'client.id': socket.gethostname()
    }

    producer = SerializingProducer(conf)
    return producer

def produce(a, b, topic):
    for i in range(a, b):
        key = f'key_{i}'
        value = {"name": f"John Doe_{i}", "age": i}

        try:
            producer.produce(topic=topic, key=key, value=value, on_delivery=delivery_report)
            producer.poll(0)
        except BufferError:
            producer.flush()
            producer.produce(topic=topic, key=key, value=value, on_delivery=delivery_report)
            producer.poll(0)


if __name__ == "__main__":
    broker_address = 'localhost:9092'
    kafka_topic = 'topic1'

    producer = kafka_producer(broker_address)

    threads = []
    total_msgs = 1_000_000
    msgs_per_thread = 100_000
    for i in range(1, total_msgs+1, msgs_per_thread):
        t = Thread(target=produce, args=([i, i+msgs_per_thread, kafka_topic]))
        threads.append(t)
        t.start()
    
    for t in threads: 
        t.join()

    producer.flush()
