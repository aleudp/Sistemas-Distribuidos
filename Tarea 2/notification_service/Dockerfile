# Base image with Python
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY notification_service.py /app/notification_service.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Run the service
CMD ["python", "/app/notification_service.py"]
