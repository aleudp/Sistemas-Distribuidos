# Use the official Cassandra image as base
FROM cassandra:latest

# Set the working directory inside the container
WORKDIR /docker-entrypoint-initdb.d

# Copy the CQL initialization script into the container's init directory
COPY init_cassandra.cql /docker-entrypoint-initdb.d/

# Expose the default ports
EXPOSE 9042 7000 7001

# Start Cassandra with the default entrypoint
CMD ["cassandra", "-f"]

