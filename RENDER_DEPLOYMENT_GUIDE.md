# 🚀 Render.com Deployment Guide

## CivicReporter Backend Deployment on Render.com

This guide will help you deploy the CivicReporter FastAPI backend to Render.com.

### 📋 Prerequisites

1. **GitHub Repository**: Your code is already pushed to: `https://github.com/SRIVELAN-CSE/CivicReporter---db`
2. **MongoDB Atlas**: Your database is configured and running
3. **Render.com Account**: Sign up at [render.com](https://render.com)

### 🔧 Render.com Configuration Settings

#### **Step 1: Create New Web Service**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `SRIVELAN-CSE/CivicReporter---db`

#### **Step 2: Basic Configuration**
```
Name: CivicReporter-db
Language: Python 3
Branch: master
Region: Oregon (US West)
Root Directory: backend
```

#### **Step 3: Build & Deploy Commands**
```bash
# Build Command
pip install -r requirements.txt

# Start Command  
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

#### **Step 4: Environment Variables**
Add these environment variables in Render:

| Variable Name | Value |
|---------------|--------|
| `MONGODB_URL` | `mongodb+srv://srivelansv2006_db_user:9YxxIF6TGmNQEsNg@civic-welfare-cluster.rts6zvy.mongodb.net/?retryWrites=true&w=majority&appName=civic-welfare-cluster` |
| `DATABASE_NAME` | `civic_welfare` |
| `SECRET_KEY` | `civic-welfare-super-secret-jwt-key-2025-production` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `HOST` | `0.0.0.0` |
| `RELOAD` | `false` |
| `PORT` | `10000` |

#### **Step 5: Advanced Settings**
```
Health Check Path: /healthz
Instance Type: Free (for testing) or Starter ($7/month for production)
Auto-Deploy: On Commit ✅
```

### 🎯 Expected Deployment Process

1. **Build Time**: 3-5 minutes
2. **First Deploy**: 5-10 minutes  
3. **Subsequent Deploys**: 2-3 minutes

### 🔍 Post-Deployment Testing

Once deployed, test these endpoints:

1. **Health Check**: `https://your-app-name.onrender.com/healthz`
2. **API Documentation**: `https://your-app-name.onrender.com/docs`
3. **Root Endpoint**: `https://your-app-name.onrender.com/`

### 🛠️ Troubleshooting

#### Common Issues:

1. **Build Failures**
   - Check that `requirements.txt` includes all dependencies
   - Verify Python version compatibility

2. **Start Failures**  
   - Ensure `app.py` file exists in backend directory
   - Check that gunicorn is in requirements.txt

3. **Database Connection Issues**
   - Verify MongoDB Atlas connection string
   - Check that IP whitelist includes `0.0.0.0/0` for Render

4. **CORS Issues**
   - Update CORS origins in `app.py` to include your Render domain

### 📱 Update Flutter App

After successful deployment, update your Flutter app's API base URL:

```dart
// In lib/services/backend_api_service.dart
class BackendApiService {
  static const String baseUrl = 'https://your-app-name.onrender.com/api';
  // Rest of your service code...
}
```

### 🎉 Success Indicators

✅ **Deployment Successful** when you see:
- Green "Live" status in Render dashboard
- Health check returns `{"status": "ok"}`
- API docs accessible at `/docs`
- MongoDB connection successful

Your CivicReporter backend will be live and ready! 🚀

---

**Note**: Replace `your-app-name` with your actual Render app name (likely `civicreporter-db`)

**Deployed URL**: `https://civicreporter-db.onrender.com`