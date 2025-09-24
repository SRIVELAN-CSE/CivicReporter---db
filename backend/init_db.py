"""
Database initialization script for MongoDB
Creates default admin user and sample data
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import connect_to_mongodb, close_mongodb_connection, get_users_collection
from models.schemas import UserInDB, UserType, Department
from utils.auth import get_password_hash

async def create_default_admin():
    """Skip creating default admin - users will register through mobile app"""
    print("⚠️  No default admin user created - register through mobile app")

async def create_sample_officers():
    """Skip creating sample officers - officers will register through mobile app"""
    print("⚠️  No sample officer users created - register through mobile app")

async def create_sample_citizen():
    """Skip creating sample citizen - citizens will register through mobile app"""
    print("⚠️  No sample citizen user created - register through mobile app")

async def initialize_database():
    """Initialize database with default data"""
    print("🚀 Starting database initialization...")
    
    try:
        # Connect to database
        await connect_to_mongodb()
        print("📦 Connected to MongoDB")
        
        # Create default users
        await create_default_admin()
        await create_sample_officers()
        await create_sample_citizen()
        
        print("✅ Database initialization completed successfully!")
        print("\n📋 Summary:")
        print("- No default users created")
        print("- Clean database ready for mobile app registrations")
        print("- All user data will be stored from mobile app usage")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
    finally:
        # Close database connection
        await close_mongodb_connection()
        print("📦 Database connection closed")

if __name__ == "__main__":
    asyncio.run(initialize_database())