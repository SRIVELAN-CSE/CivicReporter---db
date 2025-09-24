"""
Check what API endpoints are actually registered on Render.com
"""
import asyncio
import aiohttp
import json

async def check_available_endpoints():
    """Check what endpoints are available on Render.com"""
    print("🔍 Checking available endpoints on Render.com...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://civicreporter-db.onrender.com/openapi.json") as response:
                if response.status == 200:
                    openapi_spec = await response.json()
                    
                    print("📋 Available API Endpoints:")
                    print("=" * 50)
                    
                    paths = openapi_spec.get("paths", {})
                    
                    for path, methods in paths.items():
                        for method, details in methods.items():
                            summary = details.get("summary", "No description")
                            print(f"   {method.upper():6} {path:30} - {summary}")
                    
                    # Check specifically for auth endpoints
                    auth_endpoints = [path for path in paths if "/auth/" in path]
                    
                    print(f"\n🔐 Authentication endpoints found: {len(auth_endpoints)}")
                    for endpoint in auth_endpoints:
                        print(f"   - {endpoint}")
                        
                    if "/api/auth/register" in paths:
                        print("\n✅ Registration endpoint IS registered!")
                    else:
                        print("\n❌ Registration endpoint NOT found in OpenAPI spec")
                        
                else:
                    print(f"❌ Failed to get OpenAPI spec: {response.status}")
                    
    except Exception as e:
        print(f"🚨 Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_available_endpoints())