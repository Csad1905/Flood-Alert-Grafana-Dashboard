# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY ./mongo_exporter.py /app/mongo_exporter.py

# Install the required Python libraries
RUN pip install pymongo prometheus_client

# Expose the port where Prometheus will scrape the metrics
EXPOSE 8000

# Run the Python script when the container starts
ENTRYPOINT python3 /app/mongo_exporter.py
