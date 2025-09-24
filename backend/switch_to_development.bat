@echo off
echo 🔧 Switching to DEVELOPMENT mode...
echo.

REM Copy development environment file
copy .env.development .env >nul 2>&1

echo ✅ Backend configured for LOCAL development
echo 📊 Database: civic_welfare_local (MongoDB localhost)
echo 🌐 API URL: http://127.0.0.1:8000
echo.

echo 📱 To switch Flutter app to development mode:
echo    Edit lib\constants\api_constants.dart
echo    Change: static const bool isDevelopment = true;
echo.

echo 🚀 To start development server:
echo    python main.py
echo.

pause