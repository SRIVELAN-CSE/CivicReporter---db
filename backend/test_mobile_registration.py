"""
Test User Registration API Endpoint
Tests if the registration endpoint can successfully create users in MongoDB Atlas
"""
import asyncio
import json
import aiohttp
from database.mongodb import connect_to_mongodb, get_users_collection, close_mongodb_connection

async def test_user_registration():
    """Test user registration via API endpoint"""
    print("🧪 Testing User Registration API...")
    
    # Test user data
    test_user = {
        "name": "Test Mobile User",
        "email": "test.mobile@example.com",
        "password": "testpassword123",
        "phone": "+1234567890",
        "location": "Test City",
        "user_type": "public",
        "department": "others"
    }
    
    api_url = "https://civicreporter-db.onrender.com/api/auth/register"
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            print(f"📞 Sending registration request to: {api_url}")
            print(f"👤 User data: {test_user['name']} ({test_user['email']})")
            
            async with session.post(api_url, json=test_user, headers=headers) as response:
                print(f"🔍 Response status: {response.status}")
                
                if response.status == 201:
                    result = await response.json()
                    print("✅ Registration successful!")
                    print(f"📄 Response: {json.dumps(result, indent=2)}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Registration failed!")
                    print(f"📄 Error response: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"🚨 Error during registration test: {e}")
        return False

async def check_database_after_test():
    """Check if the test user was created in MongoDB Atlas"""
    print("\n🔍 Checking MongoDB Atlas for the test user...")
    
    try:
        await connect_to_mongodb()
        users_collection = get_users_collection()
        
        # Count total users
        total_users = await users_collection.count_documents({})
        print(f"👥 Total users in database: {total_users}")
        
        # Look for our test user
        test_user = await users_collection.find_one({"email": "test.mobile@example.com"})
        
        if test_user:
            print("✅ Test user found in MongoDB Atlas!")
            print(f"📋 User details:")
            print(f"   - Name: {test_user.get('name')}")
            print(f"   - Email: {test_user.get('email')}")
            print(f"   - Type: {test_user.get('user_type')}")
            print(f"   - Location: {test_user.get('location')}")
            
            # Clean up - remove test user
            await users_collection.delete_one({"email": "test.mobile@example.com"})
            print("🧹 Test user removed from database")
            
        else:
            print("❌ Test user NOT found in MongoDB Atlas")
            
    except Exception as e:
        print(f"🚨 Error checking database: {e}")
    finally:
        await close_mongodb_connection()

async def main():
    """Main test function"""
    print("🚀 Starting CivicReporter Registration Test")
    print("=" * 50)
    
    # Test the registration API
    registration_success = await test_user_registration()
    
    if registration_success:
        # Check if user was created in database
        await check_database_after_test()
    
    print("=" * 50)
    print("✅ Test completed!")

if __name__ == "__main__":
    asyncio.run(main())