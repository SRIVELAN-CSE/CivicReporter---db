@echo off
REM Setup script for the Civic Welfare Backend (Windows)

echo 🏛️  Civic Welfare Management System - Backend Setup
echo ==================================================

REM Check Python version
echo 📋 Checking Python version...
python --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install dependencies. Please check your Python environment.
    pause
    exit /b 1
)

REM Copy environment file if it doesn't exist
if not exist .env (
    echo 📝 Creating environment configuration...
    echo ✅ Please edit .env file to configure your environment.
) else (
    echo ✅ Environment file already exists.
)

REM Initialize database
echo 🗄️  Initializing database...
python utils/db_init.py
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to initialize database.
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📚 Next steps:
echo    1. Edit .env file with your configuration
echo    2. Start the server: python main.py
echo    3. Visit API docs: http://localhost:8000/docs
echo.
echo 👤 Default users created:
echo    Admin:  admin@civicwelfare.com (password: admin123)
echo    Officer: officer@civicwelfare.com (password: officer123)
echo    Citizen: citizen@civicwelfare.com (password: citizen123)
echo.
echo ⚠️  Don't forget to change default passwords in production!
pause