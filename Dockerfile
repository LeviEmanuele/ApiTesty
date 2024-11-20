# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies required for building and PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Uvicorn separately to reduce layer size (you can include this in requirements.txt as well)
RUN pip install --no-cache-dir uvicorn

# Copy the entire application code to the container
COPY . /app/

# Expose port 8000 to make the app accessible externally
EXPOSE 8000

# Define the command to run the application using Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
