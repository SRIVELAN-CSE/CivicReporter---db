# Environment Switching Guide

This guide explains how to switch between **Local Development** and **Production Cloud** environments for the CivicReporter system.

## 🏗️ System Architecture

### Development Mode (Computer Testing)
- **Frontend**: Flutter app → `http://127.0.0.1:8000`
- **Backend**: Local FastAPI server → Local MongoDB
- **Database**: MongoDB running on your computer
- **Use Case**: Testing, development, debugging on computer

### Production Mode (Mobile App)
- **Frontend**: Flutter app → `https://civicreporter-db.onrender.com`
- **Backend**: Render.com server → MongoDB Atlas
- **Database**: Cloud MongoDB Atlas cluster
- **Use Case**: Real mobile app usage, live data

---

## 🔄 Quick Switching Guide

### Backend Environment Switching

#### Switch to Development (Local)
```bash
cd backend
switch_to_development.bat
```
- ✅ Uses local MongoDB (`civic_welfare_local`)
- ✅ Runs on `127.0.0.1:8000`
- ✅ Perfect for computer testing

#### Switch to Production (Cloud)
```bash
cd backend
switch_to_production.bat
```
- ✅ Uses MongoDB Atlas (`civic_welfare`)
- ✅ Connects to Render.com
- ✅ Perfect for mobile app deployment

### Flutter App Environment Switching

Edit `lib/constants/api_constants.dart`:

#### For Development (Computer Testing)
```dart
static const bool isDevelopment = true;
```

#### For Production (Mobile App)
```dart
static const bool isDevelopment = false;
```

---

## 📊 Environment Comparison

| Feature | Development | Production |
|---------|-------------|------------|
| **Database** | Local MongoDB | MongoDB Atlas |
| **API URL** | `http://127.0.0.1:8000` | `https://civicreporter-db.onrender.com` |
| **Data Storage** | Computer local storage | Cloud database |
| **Use Case** | Testing & development | Mobile app usage |
| **Data Isolation** | Separate test data | Live production data |

---

## 🚀 Usage Scenarios

### Scenario 1: Development & Testing
1. Run `switch_to_development.bat`
2. Set Flutter `isDevelopment = true`
3. Start local MongoDB server
4. Run `python main.py` in backend
5. Test Flutter app on computer

### Scenario 2: Mobile App Deployment
1. Run `switch_to_production.bat`
2. Set Flutter `isDevelopment = false`
3. Build APK with `flutter build apk --release`
4. Install APK on mobile device
5. App connects to cloud database

---

## 🔧 Environment Files

- **`.env`**: Current active environment
- **`.env.development`**: Development configuration template
- **Backend scripts**: `switch_to_development.bat`, `switch_to_production.bat`
- **Flutter config**: `lib/constants/api_constants.dart`

---

## 💡 Best Practices

1. **Always switch both backend and Flutter** to the same environment
2. **Use development mode** for computer testing and debugging
3. **Use production mode** for mobile APK builds and real usage
4. **Keep development and production data separate**
5. **Test locally first**, then deploy to production

---

## 🔍 Verification

### Check Backend Environment
Look for console output when starting the server:
```
🔧 Running in DEVELOPMENT mode - Using LOCAL MongoDB
📊 Database: civic_welfare_local
```
or
```
🚀 Running in PRODUCTION mode - Using CLOUD MongoDB Atlas
📊 Database: civic_welfare
```

### Check Flutter Environment
Add this to your Flutter app for debugging:
```dart
import 'package:flutter_application_1/core/utils/environment_config.dart';

// In your main() function
EnvironmentConfig.printEnvironmentInfo();
```