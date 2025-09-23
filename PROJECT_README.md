# CivicReporter - Civic Welfare Management System 🏛️

A comprehensive **Flutter + MongoDB** application for crowdsourced civic issue reporting and resolution. Citizens can report civic problems, officers can manage and resolve issues, and administrators can oversee the entire system.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Flutter](https://img.shields.io/badge/Flutter-3.9.2-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)

## 🌟 Features

### 👥 Multi-User System
- **Citizens**: Report civic issues, track status, receive updates
- **Officers**: Manage department-specific reports, update status
- **Administrators**: Full system oversight, user management, analytics

### 📱 Flutter Frontend
- **Cross-platform** mobile application (Android, iOS, Web)
- **Real-time notifications** and status updates
- **Image capture** for issue documentation
- **Location services** for precise issue reporting
- **Offline support** with local storage sync
- **Smart categorization** using AI/ML

### 🚀 FastAPI Backend
- **MongoDB Atlas** cloud database
- **JWT authentication** with role-based access
- **RESTful API** with comprehensive endpoints
- **Real-time notifications** system
- **File upload** support for images
- **Admin approval** workflows
- **Comprehensive logging** and monitoring

## 🏗️ Architecture

```
📱 Flutter Mobile App
    ↕️ HTTP/REST API
🌐 FastAPI Backend Server
    ↕️ Motor/PyMongo
🗄️ MongoDB Atlas Cloud Database
```

## 🚀 Quick Start

### Prerequisites
- **Flutter SDK** 3.9.2 or higher
- **Python** 3.8 or higher
- **MongoDB Atlas** account (free tier available)
- **Git** for version control

### 1. Clone Repository
```bash
git clone https://github.com/SRIVELAN-CSE/CivicReporter---db.git
cd CivicReporter---db
```

### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env with your MongoDB Atlas connection string

# Initialize database
python init_db.py

# Start server
python main.py
```

### 3. Setup Flutter App
```bash
cd ..  # Go back to root directory

# Install Flutter dependencies
flutter pub get

# Run on your preferred platform
flutter run  # Mobile
flutter run -d chrome  # Web
```

## 🗄️ Database Schema

### Collections
- **users** - System users (citizens, officers, admins)
- **reports** - Civic issue reports with status tracking
- **notifications** - Real-time notification system
- **registration_requests** - Officer registration approvals
- **password_reset_requests** - Secure password recovery

### Sample Data
Default users created during initialization:
- **Admin**: admin@civicwelfare.com / admin123
- **Officers**: Various departments / officer123
- **Citizen**: citizen@example.com / citizen123

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get user profile

### Reports Management
- `POST /api/reports/` - Create new report
- `GET /api/reports/` - Get reports (role-based filtering)
- `PUT /api/reports/{id}/status` - Update report status
- `GET /api/reports/stats/` - Get statistics

### User Management (Admin)
- `GET /api/users/` - List all users
- `POST /api/users/registration-requests/{id}/approve` - Approve officer registration
- `POST /api/users/password-reset-requests/{id}/approve` - Approve password reset

### Notifications
- `GET /api/notifications/` - Get user notifications
- `PUT /api/notifications/{id}/read` - Mark as read
- `POST /api/notifications/broadcast` - Send broadcast (admin)

## 🛡️ Security Features

- **JWT Authentication** with role-based access control
- **Password encryption** using bcrypt
- **Input validation** with Pydantic models
- **CORS protection** configured for Flutter
- **Environment-based secrets** management

## 📊 Department Categories

- 🗑️ **Garbage Collection**
- 🚰 **Water Supply**
- 🛣️ **Road Maintenance**
- 💡 **Street Lights**
- 🌊 **Drainage Systems**
- 🏢 **Others**

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_backend.py
```

### Flutter Tests
```bash
flutter test
```

### API Documentation
Visit `http://localhost:8000/docs` when backend is running

## 📱 Supported Platforms

- ✅ **Android** (Native mobile app)
- ✅ **iOS** (Native mobile app)
- ✅ **Web** (Progressive web app)
- ✅ **Windows** (Desktop app)
- ✅ **macOS** (Desktop app)
- ✅ **Linux** (Desktop app)

## 🔧 Configuration

### Backend Environment (.env)
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=civic_welfare
SECRET_KEY=your-jwt-secret-key
PORT=8000
```

### Flutter Configuration
- Update API base URL in `lib/services/backend_api_service.dart`
- Configure app permissions in platform-specific files

## 📈 Monitoring & Analytics

- **Health Check**: `/api/health`
- **MongoDB Atlas Monitoring**: Built-in cluster monitoring
- **API Metrics**: Request/response tracking
- **Error Logging**: Comprehensive error handling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**SRIVELAN CSE**
- GitHub: [@SRIVELAN-CSE](https://github.com/SRIVELAN-CSE)
- Repository: [CivicReporter---db](https://github.com/SRIVELAN-CSE/CivicReporter---db)

## 🙏 Acknowledgments

- **Flutter Team** for the amazing cross-platform framework
- **FastAPI** for the modern Python web framework
- **MongoDB** for the flexible NoSQL database
- **Open Source Community** for inspiration and tools

---

## 📞 Support

For support and questions:
- 📧 Create an issue in this repository
- 📖 Check the API documentation at `/docs`
- 🔍 Review the comprehensive README files in each directory

**Made with ❤️ for better civic engagement and community welfare**