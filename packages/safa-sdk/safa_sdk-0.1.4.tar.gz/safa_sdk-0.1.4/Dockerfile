# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Copy the requirements dependencies into the container at /app
COPY production-requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r production-requirements.txt

# Copy the rest of the application code into the container at /app
COPY src /app/src/
ADD run.py /app/run.py

# Define the command to run the application
ENV SAFA_SDK_ROOT_PATH="/app/src"
ARG USERNAME
ARG PASSWORD

ENV CACHE_FILE_PATH="/app/local.cache"
RUN ["touch", "/app/local.cache"]

RUN ["python", "/app/run.py"]
