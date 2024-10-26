# Dockerfile for state-machine
FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Replace consumer.py with your actual script name if different
CMD ["python", "state_machine.py"]

