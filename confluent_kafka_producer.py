from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
import json
import socket


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    # else:
    #     print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def serialize_json(obj, ctx):
    return json.dumps(obj).encode('utf-8')

def kafka_producer(broker, topic):
    conf = {
        'bootstrap.servers': broker,
        'key.serializer': serialize_json,
        'value.serializer': serialize_json,
        'queue.buffering.max.messages': 1_000_000,
        'queue.buffering.max.kbytes': str(64 * 1024),
        'linger.ms': '300', # This property sets the maximum time (in milliseconds) that a producer will wait for additional messages to be batched together before sending them to the broker. A higher value can increase buffer memory usage, as messages are kept in memory for a longer time before being sent.
        'client.id': socket.gethostname()
    }

    producer = SerializingProducer(conf)
    
    for i in range(1_000_000):
        key = f'key_{i}'
        value = {"name": f"John Doe_{i}", "age": i}
        
        try:
            producer.produce(topic=topic, key=key, value=value, on_delivery=delivery_report)
            producer.poll(0)
        except BufferError: # producer queue is full
            producer.flush()

            # retry to produce current msg
            producer.produce(topic=topic, key=key, value=value, on_delivery=delivery_report)
            producer.poll(0)
    
    producer.flush()


if __name__ == "__main__":
    broker_address = 'localhost:9092'
    kafka_topic = 'topic1'
    
    kafka_producer(broker_address, kafka_topic)
