# Use the official Nginx image as a parent image
FROM nginx:latest

# Copy the Flask application code into the container
COPY app.py /usr/src/dist_app/

# Set the working directory in the container
WORKDIR /usr/src/dist_app

# Install Gunicorn
RUN pip install gunicorn

# Install Flask and any other dependencies
RUN pip install flask

# Copy Flask application files
COPY app.py .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the default environment variable
ENV SERVER_ID="Server_1"

# Command to run your server (e.g., using Gunicorn)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]