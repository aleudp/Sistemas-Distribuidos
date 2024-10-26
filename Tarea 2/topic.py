from kafka.admin import KafkaAdminClient, NewTopic

def create_topics():
    # Configure connection to the Kafka cluster
    admin_client = KafkaAdminClient(
        bootstrap_servers=['kafka1:9092', 'kafka2:9094', 'kafka3:9096'],
        client_id='topic_creator'
    )

    # Define the topics to create
    topics = [
        NewTopic(name="Procesando", num_partitions=3, replication_factor=3),
        NewTopic(name="Preparacion", num_partitions=3, replication_factor=3),
        NewTopic(name="Enviado", num_partitions=3, replication_factor=3),
        NewTopic(name="Entregado", num_partitions=3, replication_factor=3),
        NewTopic(name="Finalizado", num_partitions=3, replication_factor=3)
    ]

    # Create the topics
    admin_client.create_topics(new_topics=topics, validate_only=False)
    print("Topics created successfully.")

if __name__ == "__main__":
    create_topics()

