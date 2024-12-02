FROM bitnami/spark:3.5

# Install required tools
USER root
RUN apt-get update && apt-get install -y curl patch nano sed && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && pip install pyspark py4j kafka-python elasticsearch six 

# Copy test script and patch file
COPY cassandra.py /opt/bitnami/spark/cassandra.py
COPY elastic.py /opt/bitnami/spark/elastic.py
COPY spark.py /opt/bitnami/spark/spark.py

# Apply patch (alternative approach using sed)
RUN cd /opt/bitnami/python/lib/python3.12/site-packages/kafka/ && \
    sed -i 's/from kafka.vendor.six.moves import range/from six.moves import range/' codec.py


# Default command to run the test script
CMD ["tail", "-f", "/dev/null"]

