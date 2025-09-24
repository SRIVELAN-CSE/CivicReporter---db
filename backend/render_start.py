"""
Gunicorn configuration for Render.com deployment
"""
import os
from app import app

# Render.com specific configuration
port = int(os.environ.get("PORT", 8000))
host = "0.0.0.0"

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting CivicReporter API on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        workers=1,
        log_level="info",
        access_log=True
    )