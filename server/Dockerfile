# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

RUN pip install Flask 
COPY server.py .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV SERVER_ID=1

# Run server.py when the container launches
CMD ["python", "server.py"]
