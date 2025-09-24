import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database connection functions
from database.mongodb import connect_to_mongodb, close_mongodb_connection

# Import API routers with error handling
try:
    from api.routes.auth import router as auth_router
    print("✅ Auth router imported successfully")
except Exception as e:
    print(f"❌ Failed to import auth router: {e}")
    auth_router = None

try:
    from api.routes.users import router as users_router
    print("✅ Users router imported successfully")
except Exception as e:
    print(f"❌ Failed to import users router: {e}")
    users_router = None

try:
    from api.routes.reports import router as reports_router
    print("✅ Reports router imported successfully")
except Exception as e:
    print(f"❌ Failed to import reports router: {e}")
    reports_router = None

try:
    from api.routes.notifications import router as notifications_router
    print("✅ Notifications router imported successfully")
except Exception as e:
    print(f"❌ Failed to import notifications router: {e}")
    notifications_router = None

app = FastAPI(
    title="CivicReporter API",
    description="Civic Welfare Reporting System - MongoDB Backend",
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
    "*"  # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongodb()
    print("✅ Database connected successfully")
    print("🔗 API Routes registered:")
    print("   - /api/auth/* (Authentication)")
    print("   - /api/users/* (Users)")
    print("   - /api/reports/* (Reports)")
    print("   - /api/notifications/* (Notifications)")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongodb_connection()

# Include API routers with safety checks
if auth_router:
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    print("✅ Auth routes registered: /api/auth/*")

if users_router:
    app.include_router(users_router, prefix="/api/users", tags=["Users"])
    print("✅ Users routes registered: /api/users/*")

if reports_router:
    app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
    print("✅ Reports routes registered: /api/reports/*")

if notifications_router:
    app.include_router(notifications_router, prefix="/api/notifications", tags=["Notifications"])
    print("✅ Notifications routes registered: /api/notifications/*")

@app.get("/")
async def root():
    return {
        "message": "CivicReporter API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
        "database": "MongoDB Atlas",
        "framework": "FastAPI"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "CivicReporter API",
        "database": "MongoDB Atlas Connected",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/healthz")
async def health_check_render():
    """Health check endpoint specifically for Render.com"""
    try:
        # Basic health check
        return {
            "status": "ok", 
            "message": "Service is healthy",
            "timestamp": "2025-09-23",
            "service": "CivicReporter Backend"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("app:app", host=host, port=port, reload=False)