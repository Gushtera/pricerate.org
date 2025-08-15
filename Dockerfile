# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# We will not set a CMD or ENTRYPOINT here, as we want to run the crawler as a one-off command.
# The user will run the crawler using `docker-compose run`.
