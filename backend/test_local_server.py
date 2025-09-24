"""
Simple local server test to verify the API routes work
"""
import uvicorn
from app import app

if __name__ == "__main__":
    print("🚀 Starting local test server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health endpoint: http://localhost:8000/health")
    print("🔐 Register endpoint: http://localhost:8000/api/auth/register")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )