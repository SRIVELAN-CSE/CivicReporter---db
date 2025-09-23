"""
Test script to verify backend functionality
"""
import asyncio
import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

async def test_health_endpoint():
    """Test the health endpoint"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/api/health")
            print(f"Health Check: {response.status_code}")
            if response.status_code == 200:
                print("✅ Health check passed")
                print(json.dumps(response.json(), indent=2))
            else:
                print("❌ Health check failed")
                print(response.text)
        except Exception as e:
            print(f"❌ Connection failed: {e}")

async def test_auth_endpoints():
    """Test authentication endpoints"""
    async with httpx.AsyncClient() as client:
        # Test login
        login_data = {
            "email": "admin@civicwelfare.com",
            "password": "admin123"
        }
        
        try:
            response = await client.post(f"{BASE_URL}/api/auth/login", json=login_data)
            print(f"Login Test: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Login successful")
                data = response.json()
                token = data.get("access_token")
                print(f"User: {data['user']['name']} ({data['user']['user_type']})")
                
                # Test protected endpoint
                headers = {"Authorization": f"Bearer {token}"}
                me_response = await client.get(f"{BASE_URL}/api/auth/me", headers=headers)
                
                if me_response.status_code == 200:
                    print("✅ Protected endpoint access successful")
                    print(f"Profile: {me_response.json()['name']}")
                else:
                    print("❌ Protected endpoint failed")
                    
            else:
                print("❌ Login failed")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Auth test failed: {e}")

async def test_reports_endpoint():
    """Test reports endpoint with authentication"""
    async with httpx.AsyncClient() as client:
        # First login to get token
        login_data = {
            "email": "citizen@example.com",
            "password": "citizen123"
        }
        
        try:
            # Login
            login_response = await client.post(f"{BASE_URL}/api/auth/login", json=login_data)
            if login_response.status_code != 200:
                print("❌ Cannot test reports - login failed")
                return
                
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test creating a report
            report_data = {
                "title": "Test Report - Broken Street Light",
                "description": "Street light on Main St is not working",
                "category": "streetLights",
                "location": "Main Street",
                "address": "123 Main St",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "priority": "medium",
                "department": "streetLights",
                "reporter_name": "Jane Doe",
                "reporter_email": "citizen@example.com",
                "reporter_phone": "+1234567894"
            }
            
            create_response = await client.post(f"{BASE_URL}/api/reports/", json=report_data, headers=headers)
            print(f"Create Report: {create_response.status_code}")
            
            if create_response.status_code == 201:
                print("✅ Report creation successful")
                report_id = create_response.json().get("report_id")
                
                # Test getting reports
                get_response = await client.get(f"{BASE_URL}/api/reports/", headers=headers)
                if get_response.status_code == 200:
                    reports = get_response.json()
                    print(f"✅ Retrieved {len(reports)} reports")
                else:
                    print("❌ Failed to get reports")
            else:
                print("❌ Report creation failed")
                print(create_response.text)
                
        except Exception as e:
            print(f"❌ Reports test failed: {e}")

async def run_tests():
    """Run all tests"""
    print("🧪 Testing CivicWelfare MongoDB Backend")
    print("=" * 50)
    
    await test_health_endpoint()
    print()
    
    await test_auth_endpoints()
    print()
    
    await test_reports_endpoint()
    print()
    
    print("🏁 Tests completed!")

if __name__ == "__main__":
    print("⚠️  Make sure the backend server is running (python main.py)")
    print("⚠️  Make sure the database is initialized (python init_db.py)")
    input("Press Enter to continue...")
    
    asyncio.run(run_tests())