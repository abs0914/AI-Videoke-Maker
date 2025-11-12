FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY start.sh .

# Make start script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8080

# Set environment variable for port
ENV PORT=8080

# Run application
CMD ["./start.sh"]

