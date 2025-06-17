# Dockerfile — Containerize the AI-Powered Assistant

# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default entry point
CMD ["python", "assistant/main.py"]
