
# This Dockerfile is used to build a Docker image based on the python:3.8-slim-buster base image.
# It sets up the environment for running Python applications.
FROM python:3.8-slim-buster

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-venv \
    && apt-get clean

# Set the working directory
WORKDIR /app

COPY app .

# Copy only the requirements file to avoid copying unnecessary files
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py in unbuffered mode when the container launches
ENTRYPOINT ["python", "-u", "main.py"]
