from kafka.admin import KafkaAdminClient, NewTopic
import time

def wait_for_kafka():
    retries = 5
    for _ in range(retries):
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=['kafka1:9092'],
                client_id='topic_creator'
            )
            admin_client.list_topics()
            print("Kafka is ready.")
            return admin_client
        except Exception as e:
            print(f"Waiting for Kafka... {e}")
            time.sleep(10)
    raise RuntimeError("Kafka is not ready after retries.")

def create_topic():
    # Wait for Kafka to be ready
    admin_client = wait_for_kafka()

    # Topic configuration
    topic = NewTopic(name="waze-topic", num_partitions=1, replication_factor=1)

    try:
        # Create the topic if it doesn't exist already
        existing_topics = admin_client.list_topics()
        if "waze-topic" in existing_topics:
            print("Topic 'waze-topic' already exists.")
        else:
            admin_client.create_topics(new_topics=[topic], validate_only=False)
            print("Topic 'waze-topic' created successfully.")
    except Exception as e:
        print(f"Failed to create topic 'waze-topic': {e}")

if __name__ == "__main__":
    create_topic()

