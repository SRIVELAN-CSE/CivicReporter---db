"""
Clear Default Users Script for MongoDB Atlas

This script removes all default/sample users that might have been created 
by the init_db.py script, ensuring your database only contains real users 
who register through the mobile app.
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database.mongodb import connect_to_mongodb, close_mongodb_connection, get_users_collection

# Default emails to remove
DEFAULT_EMAILS = [
    "admin@civicwelfare.com",
    "john.smith@civicwelfare.com", 
    "sarah.johnson@civicwelfare.com",
    "mike.wilson@civicwelfare.com",
    "citizen@example.com"
]

async def clear_default_users():
    """Remove all default/sample users from the database"""
    print("🧹 Starting cleanup of default users...")
    
    users_collection = get_users_collection()
    
    # Count existing default users
    default_users = await users_collection.count_documents({
        "email": {"$in": DEFAULT_EMAILS}
    })
    
    if default_users == 0:
        print("✅ No default users found - database is already clean!")
        return
    
    print(f"🔍 Found {default_users} default users to remove")
    
    # Remove default users
    result = await users_collection.delete_many({
        "email": {"$in": DEFAULT_EMAILS}
    })
    
    if result.deleted_count > 0:
        print(f"✅ Successfully removed {result.deleted_count} default users")
        print("📱 Database is now clean and ready for mobile app users!")
    else:
        print("❌ No users were removed")
    
    # Show remaining user count
    total_users = await users_collection.count_documents({})
    print(f"👥 Total users remaining in database: {total_users}")

async def clear_sample_reports():
    """Remove any sample reports that reference default users"""
    print("🧹 Clearing sample reports...")
    
    # Import here to avoid circular imports
    from database.mongodb import get_reports_collection
    reports_collection = get_reports_collection()
    
    # Remove reports from default users
    result = await reports_collection.delete_many({
        "reporter_email": {"$in": DEFAULT_EMAILS}
    })
    
    if result.deleted_count > 0:
        print(f"✅ Removed {result.deleted_count} sample reports")
    else:
        print("✅ No sample reports found")

async def main():
    """Main cleanup function"""
    print("🚀 Starting CivicReporter database cleanup...")
    
    try:
        # Connect to database
        await connect_to_mongodb()
        print("📦 Connected to MongoDB Atlas")
        
        # Clear default users and sample data
        await clear_default_users()
        await clear_sample_reports()
        
        print("\n🎉 Database cleanup completed successfully!")
        print("📱 Your MongoDB Atlas database is now ready for mobile app users")
        print("💾 All future data will come from real user registrations and activities")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
    finally:
        # Close database connection
        await close_mongodb_connection()
        print("📦 Database connection closed")

if __name__ == "__main__":
    asyncio.run(main())