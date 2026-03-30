# Use lightweight Python image
FROM python:3.10-slim

# Install required tools
RUN apt-get update && \
    apt-get install -y zip curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN pip install --no-cache-dir awscli boto3

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Default command (Jenkins will override if needed)
CMD ["bash"]
