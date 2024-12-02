#!/bin/bash

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
while ! nc -z kafka1 9092; do
  echo "Kafka is not ready yet. Retrying in 5 seconds..."
  sleep 5
done

echo "Kafka is ready. Starting the scraper..."

# Start the Kafka topic creation
echo "Starting Kafka topic creation..."
python3 topic.py
if [ $? -ne 0 ]; then
  echo "Failed to create Kafka topics."
  exit 1
fi
echo "Kafka topics created successfully."

# Start the Waze scrapper
echo "Starting the Waze scrapper..."
python3 scrapper.py
if [ $? -ne 0 ]; then
  echo "Failed to execute the Waze scrapper."
  exit 1
fi
echo "Waze scrapper executed successfully."

