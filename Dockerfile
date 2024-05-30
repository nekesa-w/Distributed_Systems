# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory
WORKDIR /home

# Copy the requirements.txt file into the container at /home
COPY requirements.txt /home

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt
ENV SERVER_ID=1

CMD ["python", "server.py"]

