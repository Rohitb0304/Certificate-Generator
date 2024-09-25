# # Use the official Python image from the Docker Hub
# FROM python:3.9-slim

# # Set the working directory
# WORKDIR /app

# # Copy requirements.txt first for better caching
# COPY requirements.txt .

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     libreoffice \
#     unoconv \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# # Expose the port the app runs on
# EXPOSE 5000

# # Command to run the app
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt first for better caching
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    unoconv \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run Gunicorn with 3 worker processes
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
