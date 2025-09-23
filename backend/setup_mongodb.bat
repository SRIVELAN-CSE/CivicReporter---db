@echo off
echo "🚀 Setting up CivicWelfare MongoDB Backend..."

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo "❌ Python is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo "📦 Creating virtual environment..."
    python -m venv venv
)

REM Activate virtual environment
echo "🔧 Activating virtual environment..."
call venv\Scripts\activate.bat

REM Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo "⚙️ Creating .env file from template..."
    copy .env.example .env
    echo "📝 Please edit .env file with your MongoDB connection details"
)

echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Edit .env file with your MongoDB Atlas connection string"
echo "   2. Run: python init_db.py (to initialize database)"  
echo "   3. Run: python main.py (to start the server)"
echo ""
pause