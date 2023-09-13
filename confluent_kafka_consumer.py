from confluent_kafka import Consumer
import time
import json


def commit_completed(err, partitions):
    if err:
        print('ERROR:', str(err))
    # else:
    #     print("Committed partition offsets: " + str(partitions))
        
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'group1',
    'enable.auto.commit': False,
    'auto.offset.reset': 'smallest',
    'on_commit': commit_completed,
    'client.id': 'client1'
}

consumer = Consumer(conf)
topics = ['topic1']

def consume():
    try:
        consumer.subscribe(topics)
        while True:
            msg = consumer.poll(timeout=2.0) # wait for 2 seconds for any msg available to consumer
            
            if msg is None:
                break

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('Reached end of partition')
                    break
                else:
                    print('Error while consuming:', msg.error())
                    break
            else:
                # Process the received message
                obj = json.loads(msg.value().decode('utf-8'))
                print('Received message: ', obj)
                consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        print('Closing consumer.')
        consumer.close()

consume()
