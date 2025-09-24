@echo off
echo 🚀 Switching to PRODUCTION mode...
echo.

REM Copy current .env as backup
if exist .env copy .env .env.backup >nul 2>&1

REM Create production .env file
(
echo # Environment Configuration
echo # Set to 'development' for local storage, 'production' for cloud storage
echo ENVIRONMENT=production
echo.
echo # MongoDB Atlas Configuration ^(Production/Mobile^)
echo MONGODB_URL=mongodb+srv://srivelansv2006_db_user:9YxxIF6TGmNQEsNg@civic-welfare-cluster.rts6zvy.mongodb.net/?retryWrites=true^&w=majority^&appName=civic-welfare-cluster
echo DATABASE_NAME=civic_welfare
echo.
echo # Local MongoDB Configuration ^(Development/Computer^)
echo LOCAL_MONGODB_URL=mongodb://localhost:27017
echo LOCAL_DATABASE_NAME=civic_welfare_local
echo.
echo # API Configuration
echo PORT=8000
echo HOST=0.0.0.0
echo RELOAD=true
echo.
echo # JWT Configuration
echo SECRET_KEY=civic-welfare-super-secret-jwt-key-2025-production
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
echo.
echo # CORS Settings ^(Flutter app origins^)
echo CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://localhost:*"]
echo FLUTTER_WEB_ORIGIN=http://localhost:3000
echo FLUTTER_MOBILE_ORIGIN=http://10.0.2.2:8000
echo.
echo # Email Settings ^(for notifications^)
echo SMTP_SERVER=smtp.gmail.com
echo SMTP_PORT=587
echo EMAIL_USERNAME=your-email@gmail.com
echo EMAIL_PASSWORD=your-app-password
echo.
echo # File Upload Settings
echo MAX_FILE_SIZE=10485760
echo UPLOAD_DIRECTORY=./uploads
) > .env

echo ✅ Backend configured for PRODUCTION deployment
echo 📊 Database: civic_welfare (MongoDB Atlas)
echo 🌐 API URL: https://civicreporter-db.onrender.com
echo.

echo 📱 To switch Flutter app to production mode:
echo    Edit lib\constants\api_constants.dart
echo    Change: static const bool isDevelopment = false;
echo.

echo 🚀 Ready for deployment to Render.com
echo.

pause