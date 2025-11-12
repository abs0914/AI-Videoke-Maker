#!/bin/bash
# Start script for Basic Pitch Service on Railway

# Set port from environment variable or default to 8080
PORT=${PORT:-8080}

# Run gunicorn
exec gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2

