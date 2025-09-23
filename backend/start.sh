#!/bin/bash
# Start script for Render.com deployment
# This script will be used to start the FastAPI application with gunicorn

echo "🚀 Starting CivicReporter API on Render.com"
echo "📊 Using gunicorn with uvicorn workers"

# Start the application
exec gunicorn app:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 4 \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100