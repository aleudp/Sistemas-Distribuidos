from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, to_timestamp, split, expr
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, FloatType
from kafka import KafkaConsumer
from datetime import datetime  # <-- Add this import for datetime
import json
import uuid
import re
from elasticsearch import Elasticsearch

# Setup Spark session with Cassandra and Elasticsearch
spark = SparkSession.builder \
    .appName("WazeIncidentProcessor") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.cassandra.auth.username", "cassandra") \
    .config("spark.cassandra.auth.password", "cassandra") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.1.0") \
    .getOrCreate()

# Elasticsearch client setup
es = Elasticsearch(["http://elasticsearch:9200"])

# Define schema for the data
schema = StructType([
    StructField("id", StringType(), False),
    StructField("type", StringType(), True),
    StructField("position", StringType(), True),
    StructField("timestamp", StringType(), True),  # Keep timestamp as StringType initially
    StructField("date", StringType(), True),
    StructField("x_coordinate", FloatType(), True),
    StructField("y_coordinate", FloatType(), True),
    StructField("type_keywords", ArrayType(StringType()), True)
])

# Kafka configuration
BROKER_LIST = "kafka1:9092"
TOPIC = "waze-topic"

# Function to extract x and y coordinates from the position field
def extract_coordinates(position_str):
    match = re.search(r'translate3d\(([-\d]+)px,\s*([-\d]+)px', position_str)
    if match:
        x = int(match.group(1))  # x-coordinate
        y = int(match.group(2))  # y-coordinate
        return (x, y)
    return (None, None)

# Register the UDF for extracting coordinates
extract_coordinates_udf = udf(extract_coordinates, ArrayType(FloatType()))

# Function to consume messages from Kafka and process them
def consume_messages():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BROKER_LIST,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="spark-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    print("Kafka consumer started. Listening for messages...")

    for message in consumer:
        print(f"Received message: {message.value}")

        # Extract data from the message and apply transformations
        transformed_data = []
        message_data = message.value  # Single message (as a dictionary)

        transformed_data.append({
            "id": str(uuid.uuid4()),  # Generate a unique ID for each message
            "type": message_data["type"],
            "position": message_data["position"],
            "timestamp": message_data["timestamp"],  # Keep the original timestamp
            "date": datetime.fromisoformat(message_data["timestamp"]).date().strftime("%Y-%m-%d"),  # Extract date from timestamp
            "x_coordinate": None,
            "y_coordinate": None,
            "type_keywords": ["alert"]  # Adding a sample keyword list (can be extended as needed)
        })

        # Create a DataFrame with the transformed data and the defined schema
        df = spark.createDataFrame(transformed_data, schema=schema)

        # Convert the timestamp from string to timestamp format
        df_transformed = df.withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"))

        # Transform the position field to extract coordinates
        df_transformed = df_transformed.withColumn("coordinates", extract_coordinates_udf(col("position"))) \
                                       .withColumn("x_coordinate", col("coordinates").getItem(0)) \
                                       .withColumn("y_coordinate", col("coordinates").getItem(1)) \
                                       .drop("coordinates")

        # Show the transformed DataFrame (optional)
        df_transformed.show(truncate=False)

        # Check the 'type' field to route the message
        message_type = message_data["type"]

        # If type is 'hazard', 'road-closed', or 'accident', send to Elasticsearch
        if any(keyword in message_type for keyword in ["hazard", "road-closed", "accident"]):
            # Real-time data - Write to Elasticsearch
            try:
                # Format data for Elasticsearch
                for row in df_transformed.collect():
                    es_doc = {
                        "id": row["id"],
                        "type": row["type"],
                        "position": row["position"],
                        "timestamp": row["timestamp"],
                        "date": row["date"],
                        "x_coordinate": row["x_coordinate"],
                        "y_coordinate": row["y_coordinate"],
                        "type_keywords": row["type_keywords"]
                    }

                    # Write to Elasticsearch
                    es.index(index="waze_incidents", id=row["id"], body=es_doc)
                    print(f"Real-time data inserted into Elasticsearch: {es_doc}")

            except Exception as e:
                print(f"Error inserting real-time data into Elasticsearch: {e}")
        else:
            # Historical data - Write to Cassandra
            try:
                df_transformed.write \
                    .format("org.apache.spark.sql.cassandra") \
                    .options(table="waze_incidents", keyspace="waze_keyspace") \
                    .mode("append") \
                    .save()

                print(f"Historical data inserted into Cassandra: {message_data}")

            except Exception as e:
                print(f"Error inserting historical data into Cassandra: {e}")

if __name__ == "__main__":
    consume_messages()

