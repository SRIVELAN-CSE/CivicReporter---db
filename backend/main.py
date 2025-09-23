"""
Civic Welfare Management System - Backend API

This is the MongoDB backend for the Flutter civic welfare application.
It will provide REST API endpoints for managing users, reports, notifications, 
registration requests, and password reset requests.

Features:
- MongoDB Atlas database
- FastAPI for REST endpoints
- JWT authentication
- Real-time notifications support

Usage:
    python main.py

API Documentation:
    http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from datetime import datetime
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import connect_to_mongodb, close_mongodb_connection
from api.routes import auth, users, reports, notifications

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Civic Welfare Management API",
    description="Backend API for Flutter civic welfare application",
    version="1.0.0",
    contact={
        "name": "Civic Welfare Team",
        "email": "support@civicwelfare.com",
    },
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual Flutter app origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Setup MongoDB connection and include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])

# Database startup and shutdown events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongodb()
    print("📦 Connected to MongoDB!")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongodb_connection()
    print("📦 Disconnected from MongoDB!")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Civic Welfare Management API",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    from database import get_database
    
    try:
        # Test database connection
        db = get_database()
        # Simple ping to check connection
        await db.command("ping")
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "MongoDB connection successful"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,  # Set to False in production
        log_level="info"
    )