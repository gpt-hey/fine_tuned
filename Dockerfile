# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install essential tools and Python
RUN apt-get update && \
    apt-get install -y build-essential cmake gcc g++

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8081

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python3", "./server/websocket_server.py"]
