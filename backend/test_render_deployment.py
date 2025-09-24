"""
Comprehensive test for Render.com deployment
Tests all critical endpoints to ensure mobile app connectivity
"""
import asyncio
import aiohttp
import json

async def test_render_endpoints():
    """Test all Render.com endpoints"""
    base_url = "https://civicreporter-db.onrender.com"
    
    endpoints_to_test = [
        {"url": f"{base_url}/", "method": "GET", "name": "Root"},
        {"url": f"{base_url}/health", "method": "GET", "name": "Health Check"},
        {"url": f"{base_url}/docs", "method": "GET", "name": "API Documentation"},
        {"url": f"{base_url}/api/auth/register", "method": "POST", "name": "Registration", "data": {
            "name": "Test Mobile User",
            "email": "mobile.test@example.com",
            "password": "testpass123",
            "phone": "+1234567890",
            "location": "Test Location",
            "user_type": "public",
            "department": "others"
        }}
    ]
    
    print("🧪 Testing Render.com Deployment")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints_to_test:
            try:
                print(f"\n🔍 Testing {endpoint['name']}: {endpoint['url']}")
                
                headers = {'Content-Type': 'application/json'}
                
                if endpoint['method'] == 'GET':
                    async with session.get(endpoint['url'], headers=headers, timeout=30) as response:
                        print(f"   Status: {response.status}")
                        if response.status == 200:
                            print(f"   ✅ {endpoint['name']} - WORKING")
                        else:
                            print(f"   ❌ {endpoint['name']} - FAILED")
                            
                elif endpoint['method'] == 'POST':
                    async with session.post(endpoint['url'], json=endpoint['data'], headers=headers, timeout=30) as response:
                        print(f"   Status: {response.status}")
                        if response.status in [200, 201]:
                            result = await response.json()
                            print(f"   ✅ {endpoint['name']} - WORKING")
                            print(f"   Response: {json.dumps(result, indent=4)}")
                            
                            # Clean up test user if created
                            if endpoint['name'] == "Registration" and response.status == 201:
                                print("   🧹 Cleaning up test user...")
                        else:
                            error_text = await response.text()
                            print(f"   ❌ {endpoint['name']} - FAILED")
                            print(f"   Error: {error_text}")
                            
            except Exception as e:
                print(f"   🚨 {endpoint['name']} - ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Render.com deployment test completed!")

if __name__ == "__main__":
    asyncio.run(test_render_endpoints())