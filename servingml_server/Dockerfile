# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the local code to the container
COPY . .

# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fastapi[all] uvicorn

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
