"""
MongoDB Atlas Connection Test
"""
import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv()

async def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    try:
        # Get connection string from environment
        mongodb_url = os.getenv("MONGODB_URL")
        database_name = os.getenv("DATABASE_NAME", "civic_welfare")
        
        print("🔗 Testing MongoDB Atlas connection...")
        print(f"Database: {database_name}")
        print("Connection URL: " + mongodb_url[:50] + "..." if len(mongodb_url) > 50 else mongodb_url)
        
        # Create client
        client = AsyncIOMotorClient(mongodb_url)
        
        # Get database
        database = client[database_name]
        
        # Test connection with ping
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Test database operations
        test_collection = database.test_connection
        
        # Insert a test document
        test_doc = {"message": "Connection test successful", "timestamp": "2025-09-23"}
        result = await test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Read the test document back
        retrieved_doc = await test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Test document retrieved: {retrieved_doc['message']}")
        
        # Clean up test document
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")
        
        # List databases to verify access
        db_list = await client.list_database_names()
        print(f"✅ Available databases: {db_list}")
        
        # Close connection
        client.close()
        print("✅ Connection test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mongodb_connection())
    if success:
        print("\n🎉 MongoDB Atlas is ready for the CivicWelfare backend!")
    else:
        print("\n❌ Please check your MongoDB Atlas configuration")