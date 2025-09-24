"""
Production startup script for Render.com deployment
This file ensures proper FastAPI application startup with all routes
"""
import os
import uvicorn
from app import app

def main():
    """Main startup function for production deployment"""
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("🚀 CivicReporter API Starting...")
    print(f"📊 Environment: {os.getenv('ENVIRONMENT', 'production')}")
    print(f"🌐 Server: {host}:{port}")
    print(f"📚 Documentation: http://{host}:{port}/docs")
    print(f"🔗 Health Check: http://{host}:{port}/health")
    print("🔐 API Endpoints:")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - GET  /api/reports")
    print("   - POST /api/reports")
    
    # Run the application
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()