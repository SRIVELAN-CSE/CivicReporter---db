"""
Test deployment status - Check if new code is deployed
"""
import aiohttp
import asyncio

async def check_deployment_status():
    """Check if new deployment is active"""
    url = "https://civicreporter-db.onrender.com/"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                text = await response.text()
                print(f"Status: {response.status}")
                print(f"Response content: {text[:200]}...")
                
                # Check if this looks like the new deployment
                if "CivicReporter API" in text:
                    print("✅ Deployment appears to be running")
                    
                    # Now check docs endpoint for more detail
                    docs_url = "https://civicreporter-db.onrender.com/docs"
                    async with session.get(docs_url) as docs_response:
                        docs_text = await docs_response.text()
                        if "/api/auth" in docs_text:
                            print("✅ API routes appear to be in documentation")
                        else:
                            print("❌ API routes NOT found in documentation")
                            print("📋 Docs content preview:")
                            print(docs_text[:500])
                else:
                    print("❌ Deployment not responding correctly")
                    
    except Exception as e:
        print(f"🚨 Error checking deployment: {e}")

if __name__ == "__main__":
    asyncio.run(check_deployment_status())