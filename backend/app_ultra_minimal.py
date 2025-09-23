import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CivicReporter API",
    description="Civic Welfare Reporting System - Ultra Minimal Version",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "CivicReporter API is running!",
        "version": "1.0.0-ultra-minimal",
        "status": "healthy",
        "note": "Ultra minimal version for Render deployment test"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "CivicReporter API Ultra Minimal"
    }

@app.get("/healthz")
async def health_check_render():
    return {"status": "ok", "message": "Ultra minimal service is healthy"}

@app.get("/test")
async def test():
    return {
        "message": "Test endpoint working",
        "environment_vars": {
            "MONGODB_URL": "configured" if os.getenv("MONGODB_URL") else "missing",
            "PORT": os.getenv("PORT", "8000")
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app_ultra_minimal:app", host="0.0.0.0", port=port)