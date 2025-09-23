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
    """Create default admin user if none exists"""
    users_collection = get_users_collection()
    
    # Check if admin already exists
    admin_exists = await users_collection.find_one({"user_type": "admin"})
    if admin_exists:
        print("✅ Admin user already exists")
        return
    
    # Create default admin
    admin_user = UserInDB(
        name="System Administrator",
        email="admin@civicwelfare.com",
        phone="+1234567890",
        user_type=UserType.ADMIN,
        location="City Hall",
        department=Department.OTHERS,
        password_hash=get_password_hash("admin123")  # Change this password!
    )
    
    admin_dict = admin_user.dict()
    result = await users_collection.insert_one(admin_dict)
    
    if result.inserted_id:
        print("✅ Default admin user created successfully!")
        print("📧 Email: admin@civicwelfare.com")
        print("🔑 Password: admin123 (CHANGE THIS IN PRODUCTION!)")
    else:
        print("❌ Failed to create admin user")

async def create_sample_officers():
    """Create sample officer users for testing"""
    users_collection = get_users_collection()
    
    # Check if officers already exist
    officer_exists = await users_collection.find_one({"user_type": "officer"})
    if officer_exists:
        print("✅ Officer users already exist")
        return
    
    officers = [
        {
            "name": "John Smith",
            "email": "john.smith@civicwelfare.com",
            "phone": "+1234567891",
            "department": Department.ROAD_MAINTENANCE,
            "location": "Municipal Building"
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@civicwelfare.com", 
            "phone": "+1234567892",
            "department": Department.WATER_SUPPLY,
            "location": "Water Department"
        },
        {
            "name": "Mike Wilson",
            "email": "mike.wilson@civicwelfare.com",
            "phone": "+1234567893", 
            "department": Department.GARBAGE_COLLECTION,
            "location": "Waste Management Office"
        }
    ]
    
    for officer_data in officers:
        officer_user = UserInDB(
            name=officer_data["name"],
            email=officer_data["email"],
            phone=officer_data["phone"],
            user_type=UserType.OFFICER,
            location=officer_data["location"],
            department=officer_data["department"],
            password_hash=get_password_hash("officer123")  # Change this password!
        )
        
        officer_dict = officer_user.dict()
        result = await users_collection.insert_one(officer_dict)
        
        if result.inserted_id:
            print(f"✅ Created officer: {officer_data['name']} ({officer_data['department'].value})")
        else:
            print(f"❌ Failed to create officer: {officer_data['name']}")

async def create_sample_citizen():
    """Create a sample citizen user for testing"""
    users_collection = get_users_collection()
    
    # Check if citizen already exists  
    citizen_exists = await users_collection.find_one({
        "user_type": "public",
        "email": "citizen@example.com"
    })
    if citizen_exists:
        print("✅ Sample citizen user already exists")
        return
    
    citizen_user = UserInDB(
        name="Jane Doe",
        email="citizen@example.com", 
        phone="+1234567894",
        user_type=UserType.PUBLIC,
        location="Downtown Area",
        password_hash=get_password_hash("citizen123")  # Change this password!
    )
    
    citizen_dict = citizen_user.dict()
    result = await users_collection.insert_one(citizen_dict)
    
    if result.inserted_id:
        print("✅ Created sample citizen user")
        print("📧 Email: citizen@example.com")
        print("🔑 Password: citizen123")
    else:
        print("❌ Failed to create citizen user")

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
        print("- Admin user: admin@civicwelfare.com / admin123")
        print("- Officer users: *.officer@civicwelfare.com / officer123")
        print("- Citizen user: citizen@example.com / citizen123")
        print("\n⚠️  IMPORTANT: Change default passwords in production!")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
    finally:
        # Close database connection
        await close_mongodb_connection()
        print("📦 Database connection closed")

if __name__ == "__main__":
    asyncio.run(initialize_database())