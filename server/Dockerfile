# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY server.py .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV SERVER_ID=1

# Run server.py when the container launches
CMD ["python", "server.py"]
