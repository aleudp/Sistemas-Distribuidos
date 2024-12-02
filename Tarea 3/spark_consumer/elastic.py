from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp, date_format, split
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from elasticsearch import Elasticsearch
import json

# Setup Spark session
spark = SparkSession.builder \
    .appName("WazeIncidentProcessor") \
    .config("spark.es.nodes", "elasticsearch:9200") \
    .config("spark.es.port", "9200") \
    .config("spark.es.index.auto.create", "true") \
    .getOrCreate()

# Elasticsearch client setup
es = Elasticsearch(["http://elasticsearch:9200"])

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
        
        # Send data to Elasticsearch
        try:
            # Prepare document
            for row in df_filtered.collect():
                doc = {
                    "type": row["type"],
                    "position": row["position"],
                    "timestamp": row["timestamp"],
                    "date": row["date"],
                    "x_coordinate": row["x_coordinate"],
                    "y_coordinate": row["y_coordinate"],
                    "type_keywords": row["type_keywords"]  # List of keywords as a field
                }
                
                # Index data in Elasticsearch
                es.index(index="waze-incidents", doc_type="_doc", body=doc)
                print(f"Document indexed in Elasticsearch: {doc}")
        except Exception as e:
            print(f"Error indexing document in Elasticsearch: {e}")

if __name__ == "__main__":
    consume_messages()


