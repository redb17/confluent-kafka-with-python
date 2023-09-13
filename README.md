# Dockerfile for Confluent-Kafka Producer and Consumer Python Scripts inside Ubuntu Docker Image

```sh
docker build --progress=plain -t properbinaries/confluent_kafka:1.0.0 .
# or pull from Dockerhub
docker pull properbinaries/confluent_kafka:1.0.0
```

Spawn a container from the built image, start the zookeeper, broker and run the python files for producer and consumer. 
There is another producer script with multithreading for producing messages concurrently.

## Confluent Kafka Commands
```sh
# start zookeeper
/home/confluent-7.5.0/bin/zookeeper-server-start /home/confluent-7.5.0/etc/kafka/zookeeper.properties

# start kafka broker
/home/confluent-7.5.0/bin/kafka-server-start /home/confluent-7.5.0/etc/kafka/server.properties

# create a topic
/home/confluent-7.5.0/bin/kafka-topics --create --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --topic topic_name
```
