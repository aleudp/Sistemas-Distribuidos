from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime
import json
import threading

# Initialize the Elasticsearch client
es = Elasticsearch("http://elasticsearch:9200")

def get_current_millis():
    # Get the current time in epoch milliseconds
    return int(datetime.utcnow().timestamp() * 1000)

def consume_and_index(topic_name, doc):
    # Get the current time in epoch milliseconds
    current_time = get_current_millis()

    # Check if the document already exists in Elasticsearch
    if es.exists(index="products", id=doc["ID"]):
        # Retrieve the existing document
        existing_doc = es.get(index="products", id=doc["ID"])["_source"]
    else:
        # Initialize a new document if it doesn't exist
        existing_doc = {
            "product_name": doc["product_name"],
            "price": doc["price"],
            "ID": doc["ID"],
            "payment_method": doc["payment_method"],
            "card_brand": doc["card_brand"],
            "bank": doc["bank"],
            "region": doc["region"],
            "address": doc["address"],
            "email": doc["email"],
            "start_time": current_time,  # Initial start time in epoch milliseconds
            # Initialize topic-specific timestamps with entry_time in epoch milliseconds
            "Procesando": {"entry_time": None},
            "Preparacion": {"entry_time": None, "latency": None},
            "Finalizado": {"entry_time": None, "latency": None},
            "Enviado": {"entry_time": None, "latency": None},
            "Entregado": {"entry_time": None, "latency": None}
        }

    # Access topic data for this document
    topic_data = existing_doc[topic_name]

    # Set entry time if this is the first time the document enters the topic
    if topic_data["entry_time"] is None:
        topic_data["entry_time"] = current_time

        # Calculate latency for transitions by checking previous stage's entry_time
        stages = ["Procesando", "Preparacion", "Finalizado", "Enviado", "Entregado"]
        stage_index = stages.index(topic_name)
        if stage_index > 0:
            # Get the previous stage's entry_time
            previous_stage = stages[stage_index - 1]
            previous_entry_time = existing_doc[previous_stage]["entry_time"]
            if previous_entry_time is not None:
                # Calculate and store latency in milliseconds
                topic_data["latency"] = current_time - previous_entry_time

    # Index or update the document in Elasticsearch
    response = es.index(index="products", id=doc["ID"], document=existing_doc)
    print(f"Document indexed/updated for topic {topic_name}: {response}")

def start_consumer(topic_name):
    # Kafka brokers list for redundancy
    kafka_brokers = ["kafka1:9092", "kafka2:9092", "kafka3:9092"]

    # Set up Kafka consumer for the specified topic
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=kafka_brokers,
        group_id=f"consumer-{topic_name}",  # Unique group ID per topic
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
    
    print(f"Consumer started for topic: {topic_name}")

    # Continuously consume messages
    for message in consumer:
        doc = message.value
        consume_and_index(topic_name, doc)

def start_consumer_group():
    # Topics to be consumed
    topics = ["Procesando", "Preparacion", "Finalizado", "Enviado", "Entregado"]
    
    # Start a separate thread for each topic consumer
    for topic in topics:
        thread = threading.Thread(target=start_consumer, args=(topic,))
        thread.start()
        print(f"Thread started for consumer on topic: {topic}")

# Run the consumer group
if __name__ == "__main__":
    if es.ping():
        print("Connected to Elasticsearch")
        start_consumer_group()
    else:
        print("Could not connect to Elasticsearch.")
