import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

app = FastAPI(
    title="CivicReporter API",
    description="Civic Welfare Reporting System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for production
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "https://civicreporter-db.onrender.com",
    "https://*.onrender.com",
    "*"  # Allow all origins for now
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic endpoints for testing
@app.get("/")
async def root():
    return {
        "message": "CivicReporter API is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy",
        "database": "MongoDB Atlas",
        "framework": "FastAPI"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "CivicReporter API",
        "database": "MongoDB Atlas",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/healthz")
async def health_check_render():
    """Health check endpoint specifically for Render.com"""
    try:
        return {
            "status": "ok", 
            "message": "Service is healthy",
            "timestamp": "2025-09-23",
            "service": "CivicReporter Backend"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Test MongoDB connection endpoint
@app.get("/api/test")
async def test_connection():
    """Test endpoint to verify deployment"""
    try:
        mongodb_url = os.getenv("MONGODB_URL")
        if mongodb_url:
            return {
                "status": "success",
                "message": "MongoDB URL configured",
                "database": "civic_welfare",
                "environment": os.getenv("ENVIRONMENT", "production")
            }
        else:
            return {
                "status": "warning",
                "message": "MongoDB URL not configured",
                "note": "Add MONGODB_URL environment variable"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("app_simple:app", host=host, port=port, reload=False)