import threading
import time
import random
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

TOPICS = ['Procesando', 'Preparacion', 'Finalizado', 'Enviado', 'Entregado']

def create_producer():
    """Create a Kafka producer with retries."""
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=['kafka1:9092', 'kafka2:9094', 'kafka3:9096'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Producer connected successfully.")
            return producer
        except NoBrokersAvailable:
            print("Error: No brokers available for producer. Retrying in 5 seconds...")
            time.sleep(5)

def create_consumer(topic):
    """Create a Kafka consumer with retries."""
    while True:
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=['kafka1:9092', 'kafka2:9094', 'kafka3:9096'],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id=f'{topic}_group',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            print(f"Consumer for {topic} connected successfully.")
            return consumer
        except NoBrokersAvailable:
            print(f"Error: No brokers available for {topic}. Retrying in 5 seconds...")
            time.sleep(5)

def consume_and_produce(topic_index):
    """Consume messages from a topic and produce to the next one in the state machine."""
    current_topic = TOPICS[topic_index]
    next_topic = TOPICS[topic_index + 1] if topic_index + 1 < len(TOPICS) else None
    consumer = create_consumer(current_topic)
    producer = create_producer()

    for message in consumer:
        print(f"Consumed message from {current_topic}: {message.value}")
        time.sleep(random.uniform(0, 1))  # Random delay between 0 and 1 seconds
        
        if next_topic:
            producer.send(next_topic, message.value)
            print(f"Produced message to {next_topic}: {message.value}")
        else:
            print("Reached the final state 'Entregado'. No further production.")
            break  # Stop processing if there is no next topic


def start_state_machine():
    """Start separate threads for each topic to act as state machine consumers/producers."""
    threads = []
    for i in range(len(TOPICS)):
        thread = threading.Thread(target=consume_and_produce, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    start_state_machine()

