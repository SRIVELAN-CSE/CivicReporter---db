#!/bin/bash
# Setup script for the Civic Welfare Backend

echo "🏛️  Civic Welfare Management System - Backend Setup"
echo "=================================================="

# Check Python version
echo "📋 Checking Python version..."
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python environment."
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment configuration..."
    cp .env .env.backup 2>/dev/null || true
    echo "✅ Please edit .env file to configure your environment."
else
    echo "✅ Environment file already exists."
fi

# Initialize database
echo "🗄️  Initializing database..."
python utils/db_init.py
if [ $? -ne 0 ]; then
    echo "❌ Failed to initialize database."
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📚 Next steps:"
echo "   1. Edit .env file with your configuration"
echo "   2. Start the server: python main.py"
echo "   3. Visit API docs: http://localhost:8000/docs"
echo ""
echo "👤 Default users created:"
echo "   Admin:  admin@civicwelfare.com (password: admin123)"
echo "   Officer: officer@civicwelfare.com (password: officer123)"
echo "   Citizen: citizen@civicwelfare.com (password: citizen123)"
echo ""
echo "⚠️  Don't forget to change default passwords in production!"