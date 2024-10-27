# Dockerfile.elastic
FROM python:3.10

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the elastic.py script
COPY elastic.py .

CMD ["python", "elastic.py"]
