FROM python:3.9-slim

# Install necessary tools
RUN apt-get update && apt-get install -y \
    wget \
    firefox-esr \
    bash \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.35.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.35.0-linux64.tar.gz

# Install Python dependencies
RUN pip install --no-cache-dir selenium confluent-kafka kafka-python

# Copy the Python scripts
COPY topic.py /app/topic.py
COPY scrapper.py /app/scrapper.py

# Copy the main shell script
COPY main.sh /app/main.sh
RUN chmod +x /app/main.sh

# Set the working directory
WORKDIR /app

# Default command to run main.sh
CMD ["/bin/bash", "main.sh"]

