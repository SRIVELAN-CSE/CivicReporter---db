# Render.com Alternative Configuration
# Use this configuration in Render if the main approach fails

## Build Command:
```bash
pip install --upgrade pip && pip install --only-binary=all -r requirements-wheels.txt
```

## Start Command:
```bash
gunicorn app_simple:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

## Root Directory:
```
backend
```

## Environment Variables:
```
MONGODB_URL = mongodb+srv://srivelansv2006_db_user:9YxxIF6TGmNQEsNg@civic-welfare-cluster.rts6zvy.mongodb.net/?retryWrites=true&w=majority&appName=civic-welfare-cluster
DATABASE_NAME = civic_welfare
SECRET_KEY = civic-welfare-super-secret-jwt-key-2025-production
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
HOST = 0.0.0.0
RELOAD = false
```

## Alternative Build Commands (try in order):

1. **First Try:**
```bash
pip install --upgrade pip && pip install --only-binary=all -r requirements-wheels.txt
```

2. **If that fails:**
```bash
pip install --upgrade pip && pip install --no-deps -r requirements-wheels.txt
```

3. **Last resort:**
```bash
pip install --upgrade pip && pip install fastapi uvicorn pymongo pydantic python-multipart PyJWT python-dotenv email-validator gunicorn
```

The simplified app_simple.py has minimal dependencies and should deploy successfully.