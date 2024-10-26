import json
import time
from datetime import datetime
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

# Kafka topics
TOPICS = ['Procesando', 'Preparacion', 'Finalizado', 'Enviado', 'Entregado']

# Elasticsearch setup
es = Elasticsearch(['http://elasticsearch:9200'])

def create_consumer(topic):
    """Create a Kafka consumer for the specified topic."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=['kafka1:9092', 'kafka2:9094', 'kafka3:9096'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=f'{topic}_group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

def send_to_elasticsearch(topic, message):
    """Send the message to Elasticsearch with added metadata."""
    index_name = message['id']
    timestamp = datetime.utcnow().isoformat()

    # Adding metadata fields
    message['timestamp'] = timestamp
    message['topic'] = topic

    # Index the document in Elasticsearch
    es.index(index="messages", id=index_name, body=message)
    print(f"Indexed message to Elasticsearch: {message}")

def consume_topic(topic):
    """Consume messages from a Kafka topic and send to Elasticsearch."""
    consumer = create_consumer(topic)

    for message in consumer:
        print(f"Consumed message from {topic}: {message.value}")
        send_to_elasticsearch(topic, message.value)

if __name__ == '__main__':
    # Start consuming each topic in separate threads
    for topic in TOPICS:
        consume_topic(topic)

