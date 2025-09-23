"""
Civic Welfare Management System - Backend API

This is the MongoDB backend for the Flutter civic welfare application.
It provides REST API endpoints for managing users, reports, notifications, 
registration requests, and password reset requests.

Features:
- MongoDB Atlas database
- FastAPI for REST endpoints
- JWT authentication
- Real-time notifications support

Usage:
    python main.py (for local development)
    For production: Use app.py with gunicorn

API Documentation:
    http://localhost:8000/docs
"""

import os
import uvicorn
from app import app

if __name__ == "__main__":
    # Local development configuration
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print(f"� Starting CivicReporter API on {host}:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )