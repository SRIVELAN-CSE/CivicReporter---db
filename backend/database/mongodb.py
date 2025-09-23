"""
MongoDB Database Configuration and Connection Management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "civic_welfare")

# Global database client instance
client: Optional[AsyncIOMotorClient] = None
database = None

async def connect_to_mongodb():
    """Create database connection"""
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    print(f"Connected to MongoDB: {DATABASE_NAME}")

async def close_mongodb_connection():
    """Close database connection"""
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return database

# Collections
def get_users_collection():
    return database.users

def get_reports_collection():
    return database.reports

def get_notifications_collection():
    return database.notifications

def get_registration_requests_collection():
    return database.registration_requests

def get_password_reset_requests_collection():
    return database.password_reset_requests

def get_need_requests_collection():
    return database.need_requests