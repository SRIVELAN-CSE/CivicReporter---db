# 🔄 Environment Switching System - Quick Reference

Your CivicReporter system now supports seamless switching between local development and cloud production environments.

## 🎯 Two Modes Available

### 1. **Development Mode** (Computer Testing)
- **Database**: Local MongoDB on your computer
- **API**: `http://127.0.0.1:8000` 
- **Data**: Stored locally for testing
- **Use**: Development, debugging, computer testing

### 2. **Production Mode** (Mobile App)
- **Database**: MongoDB Atlas (cloud)
- **API**: `https://civicreporter-db.onrender.com`
- **Data**: Stored in cloud for real users
- **Use**: Mobile app deployment, real usage

---

## ⚡ Quick Switch Commands

### Switch Backend Environment

**To Development (Local):**
```bash
cd backend
.\switch_to_development.bat
```

**To Production (Cloud):**
```bash
cd backend
.\switch_to_production.bat
```

### Switch Flutter App

Edit `lib/constants/api_constants.dart`:

**For Development:**
```dart
static const bool isDevelopment = true;  // Local testing
```

**For Production:**
```dart
static const bool isDevelopment = false; // Mobile app
```

---

## 🚀 Common Usage Scenarios

### **Computer Development & Testing**
1. Run `.\switch_to_development.bat`
2. Set Flutter `isDevelopment = true`
3. Start local backend: `python main.py`
4. Test app on computer with local data

### **Mobile App Deployment**
1. Run `.\switch_to_production.bat` 
2. Set Flutter `isDevelopment = false`
3. Build APK: `flutter build apk --release`
4. Install APK on phone - connects to cloud

---

## 📊 What Gets Switched

| Component | Development | Production |
|-----------|-------------|------------|
| **Backend Database** | Local MongoDB | MongoDB Atlas |
| **Flutter API Calls** | `127.0.0.1:8000` | `civicreporter-db.onrender.com` |
| **Data Storage** | Computer local | Cloud database |
| **Environment File** | `.env.development` | `.env` (production) |

---

## ✅ Verification

After switching, verify the configuration:

**Backend Environment:**
```bash
python -c "from database.mongodb import ENVIRONMENT, DATABASE_NAME; print(f'Mode: {ENVIRONMENT}'); print(f'Database: {DATABASE_NAME}')"
```

**Expected Output:**
- Development: `Mode: development, Database: civic_welfare_local`
- Production: `Mode: production, Database: civic_welfare`

---

## 🔒 Data Separation

- **Development data** stays on your computer (safe for testing)
- **Production data** stays in MongoDB Atlas (real user data)
- **No data mixing** between environments
- **Clean separation** for development vs production

Your system is now ready with complete environment switching! 🎉