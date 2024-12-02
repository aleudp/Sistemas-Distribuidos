from pyspark.sql.functions import expr
from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp, date_format, split
from pyspark.sql.types import StructType, StructField, StringType
from uuid import uuid4
import json

# Setup Spark session with Cassandra
spark = SparkSession.builder \
    .appName("WazeIncidentProcessor") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.cassandra.auth.username", "cassandra") \
    .config("spark.cassandra.auth.password", "cassandra") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.1.0") \
    .getOrCreate()

# Define the schema for Kafka messages
schema = StructType([
    StructField("type", StringType(), True),
    StructField("position", StringType(), True),
    StructField("timestamp", StringType(), True),  # Keep timestamp as StringType initially
])

# Kafka configuration
BROKER_LIST = "kafka1:9092"
TOPIC = "waze-topic"

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

        # Create Spark DataFrame from Kafka message
        df = spark.createDataFrame([message.value], schema=schema)

        # Convert the timestamp to proper timestamp type and format as string
        df = df.withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"))
        df = df.withColumn("timestamp", date_format(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"))  # Format as string

        # Filter data based on 'type' field (e.g., focusing on specific incidents)
        incident_types = ['accident', 'road-closed', 'hazard']  # Example categories to focus on
        df_filtered = df.filter(
            df['type'].rlike('|'.join(incident_types))  # Filter rows where 'type' matches the categories
        )

        # Extract relevant data for graphing (e.g., timestamp for trend analysis, position for geospatial analysis)
        df_filtered = df_filtered.withColumn(
            "date", date_format(col("timestamp"), "yyyy-MM-dd")
        )

        # For position, extracting x and y coordinates (assuming position is in 'transform' format)
        df_filtered = df_filtered.withColumn(
            "coordinates", split(col("position"), "transform: translate3d\\(")[1]
        )
        df_filtered = df_filtered.withColumn(
            "coordinates", split(col("coordinates"), "px")[0]
        )
        df_filtered = df_filtered.withColumn(
            "x_coordinate", split(col("coordinates"), ",")[0]
        )
        df_filtered = df_filtered.withColumn(
            "y_coordinate", split(col("coordinates"), ",")[1]
        )

        # Split the 'type' into separate keywords
        df_filtered = df_filtered.withColumn(
            "type_keywords", split(col("type"), " ")
        )

        # Prepare data for Cassandra
        df_filtered = df_filtered.withColumn("id", expr("uuid()").cast("uuid"))
        df_filtered.show(5)  # Show first 5 rows to verify the data
        df_filtered.printSchema()  # Print the schema to verify column types

        # Check schema to ensure 'id' column exists
        df_filtered.printSchema()
        # Send data to Cassandra
        try:
            # Write data to Cassandra
            for row in df_filtered.collect():
                cassandra_doc = {
                    "id": row["id"],
                    "type": row["type"],
                    "position": row["position"],
                    "timestamp": row["timestamp"],
                    "date": row["date"],
                    "x_coordinate": row["x_coordinate"],
                    "y_coordinate": row["y_coordinate"],
                    "type_keywords": row["type_keywords"]
                }

                # Write to Cassandra
                df_row = spark.createDataFrame([cassandra_doc], schema=schema)
                df_row.write \
                    .format("org.apache.spark.sql.cassandra") \
                    .options(table="waze_incidents", keyspace="waze_keyspace") \
                    .mode("append") \
                    .save()

                print(f"Document inserted into Cassandra: {cassandra_doc}")

        except Exception as e:
            print(f"Error inserting document into Cassandra: {e}")

if __name__ == "__main__":
    consume_messages()

