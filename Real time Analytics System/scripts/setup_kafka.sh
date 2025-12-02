#!/bin/bash

echo "Setting up Kafka..."

# Start Zookeeper
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties &

sleep 5

# Start Kafka
kafka-server-start /usr/local/etc/kafka/server.properties &

sleep 5

# Create topic
kafka-topics --create \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

echo "Kafka setup complete!"
