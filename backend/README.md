# Civic Welfare Management System - MongoDB Backend

This is a MongoDB-based backend for the Flutter civic welfare application. It provides a comprehensive REST API for managing users, reports, notifications, registration requests, and password reset requests.

## 🚀 Features

- **MongoDB Atlas Database** with Pymongo/Motor for async operations
- **FastAPI** REST API with automatic OpenAPI documentation
- **JWT Authentication** with role-based access control
- **User Management** (Public Citizens, Officers, Admins)
- **Report Management** with status tracking and assignments
- **Real-time Notifications** system
- **Registration Approval** workflow for officers
- **Password Reset** request system
- **Comprehensive API** with filtering, pagination, and permissions

## 🏗️ Architecture

### User Roles
- **Public Citizens**: Can create reports and view their own submissions
- **Officers**: Can view and manage reports in their department
- **Admins**: Full system access including user management

### Core Entities
- **Users**: System users with role-based permissions
- **Reports**: Civic issue reports with status tracking
- **Notifications**: In-app notification system
- **Registration Requests**: Officer registration approval workflow
- **Password Reset Requests**: Secure password recovery system

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account (free tier available)
- pip package manager

## ⚙️ Quick Setup

### 1. Environment Setup

```bash
# Run the setup script
setup_mongodb.bat

# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Configuration

1. Create a MongoDB Atlas cluster (free at https://cloud.mongodb.com)
2. Get your connection string
3. Copy `.env.example` to `.env`
4. Update the `.env` file:

```env
MONGODB_URL=mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=civic_welfare
SECRET_KEY=your-super-secret-jwt-key-here
```

### 3. Initialize Database

```bash
python init_db.py
```

This creates default users:
- **Admin**: admin@civicwelfare.com / admin123
- **Officers**: Various departments / officer123  
- **Citizen**: citizen@example.com / citizen123

### 4. Start the Server

```bash
python main.py
```

Server will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 📚 API Endpoints

### Authentication (`/api/auth`)
- `POST /login` - User authentication
- `POST /register` - User registration
- `GET /me` - Get current user profile
- `POST /refresh` - Refresh access token
- `POST /logout` - User logout

### Reports (`/api/reports`)
- `POST /` - Create new report
- `GET /` - Get reports (filtered by role)
- `GET /{report_id}` - Get specific report
- `PUT /{report_id}/status` - Update report status (officers/admins)
- `GET /stats/summary` - Get report statistics

### Users (`/api/users`)
- `GET /` - Get all users (admin only)
- `GET /{user_id}` - Get specific user
- `PUT /{user_id}/activate` - Activate user (admin)
- `PUT /{user_id}/deactivate` - Deactivate user (admin)
- `GET /registration-requests/` - Get registration requests (admin)
- `POST /registration-requests/{id}/approve` - Approve registration
- `POST /registration-requests/{id}/reject` - Reject registration
- `POST /password-reset-requests/` - Create password reset request
- `GET /password-reset-requests/` - Get password reset requests (admin)
- `POST /password-reset-requests/{id}/approve` - Approve password reset
- `POST /password-reset-requests/{id}/reject` - Reject password reset

### Notifications (`/api/notifications`)
- `POST /` - Create notification (admin)
- `GET /` - Get user's notifications
- `GET /{notification_id}` - Get specific notification
- `PUT /{notification_id}/read` - Mark as read
- `PUT /mark-all-read` - Mark all as read
- `DELETE /{notification_id}` - Delete notification
- `GET /stats/unread-count` - Get unread count
- `POST /broadcast` - Send broadcast notification (admin)
- `GET /admin/all` - Get all notifications (admin)

## 🔐 Authentication

The API uses JWT Bearer tokens. Include the token in requests:

```http
Authorization: Bearer <your_jwt_token>
```

### Login Example

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@civicwelfare.com",
  "password": "admin123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1Q...",
  "token_type": "bearer",
  "user": {
    "id": "admin_12345",
    "name": "System Administrator",
    "email": "admin@civicwelfare.com",
    "user_type": "admin"
  }
}
```

## 📊 Data Models

### User
```json
{
  "id": "uuid",
  "name": "string",
  "email": "email",
  "phone": "string", 
  "user_type": "public|officer|admin",
  "location": "string",
  "department": "garbageCollection|drainage|roadMaintenance|...",
  "is_active": true,
  "created_at": "datetime",
  "last_login_at": "datetime"
}
```

### Report
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "category": "string",
  "location": "string",
  "address": "string",
  "latitude": 0.0,
  "longitude": 0.0,
  "status": "submitted|notSeen|resolveSoon|inProgress|done|rejected|closed",
  "priority": "low|medium|high|critical",
  "department": "string",
  "reporter_id": "uuid",
  "reporter_name": "string",
  "assigned_officer_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime",
  "updates": []
}
```

## 🛠️ Development

### Project Structure
```
backend/
├── api/
│   └── routes/          # API route handlers
├── database/            # MongoDB connection and config
├── models/              # Pydantic data models
├── utils/               # Authentication and utilities
├── main.py              # FastAPI application
├── init_db.py           # Database initialization
└── requirements.txt     # Python dependencies
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### API Documentation
- Interactive docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

## 🔒 Security Considerations

1. **Change default passwords** in production
2. **Use strong JWT secret key**
3. **Enable MongoDB authentication**
4. **Configure CORS** for production domains
5. **Use HTTPS** in production
6. **Regular security updates**

## 🚀 Deployment

### MongoDB Atlas
1. Create production cluster
2. Configure IP whitelist
3. Create database user
4. Update connection string

### Environment Variables
```env
MONGODB_URL=mongodb+srv://prod_user:password@cluster.mongodb.net/
DATABASE_NAME=civic_welfare_prod
SECRET_KEY=super-secure-production-key
PORT=8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## 🤝 Integration with Flutter App

The Flutter app expects the backend at `http://127.0.0.1:8000/api`. Key integration points:

1. **Authentication**: Login/register endpoints
2. **Report Creation**: POST /api/reports/
3. **Report Fetching**: GET /api/reports/
4. **Status Updates**: Real-time via polling or webhooks
5. **Notifications**: GET /api/notifications/

## 📝 Changelog

### v1.0.0 - MongoDB Migration
- ✅ Migrated from SQLite to MongoDB Atlas
- ✅ Implemented async database operations
- ✅ Created comprehensive API endpoints
- ✅ Added role-based access control
- ✅ Integrated with existing Flutter frontend
- ✅ Added database initialization scripts

## 🆘 Troubleshooting

### Common Issues

**Database Connection Failed**
- Check MongoDB Atlas connection string
- Verify IP whitelist includes your IP
- Ensure database user has proper permissions

**Authentication Errors**
- Verify JWT secret key is set
- Check token expiration (30 minutes default)
- Ensure user is active in database

**Permission Denied**
- Check user role and permissions
- Verify JWT token is valid
- Ensure user has access to requested resource

### Logs and Debugging
- Enable debug logging in `.env`: `LOG_LEVEL=DEBUG`
- Check MongoDB Atlas logs for connection issues
- Use `/api/health` endpoint to verify connectivity

## 📞 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review error messages and status codes
3. Verify database connectivity
4. Check user permissions and authentication

## 📄 License

This project is part of the Civic Welfare Management System.

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. **Initialize database:**
   ```bash
   python utils/db_init.py
   ```

5. **Start the server:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

### Default Users

After initialization, these demo users are created:

- **Admin:** admin@civicwelfare.com (password: admin123)
- **Officer:** officer@civicwelfare.com (password: officer123)  
- **Citizen:** citizen@civicwelfare.com (password: citizen123)

⚠️ **Change these passwords in production!**

## API Documentation

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Authentication

All endpoints (except login/register) require JWT authentication:

```http
Authorization: Bearer <your_jwt_token>
```

### Base Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/api/health` | Health check |

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/register` | User registration |
| GET | `/api/auth/me` | Current user info |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/refresh` | Refresh token |

### User Management (Admin Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | Get all users |
| GET | `/api/users/registration-requests` | Get pending registrations |
| POST | `/api/users/registration-requests/{id}/approve` | Approve/reject registration |
| GET | `/api/users/password-reset-requests` | Get password reset requests |
| POST | `/api/users/password-reset-requests/{id}/approve` | Approve/reject password reset |
| POST | `/api/users/{id}/deactivate` | Deactivate user |
| POST | `/api/users/{id}/activate` | Activate user |

### Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/reports/` | Create new report |
| GET | `/api/reports/` | Get reports (filtered by role) |
| GET | `/api/reports/{id}` | Get specific report |
| PUT | `/api/reports/{id}` | Update report (Officer/Admin) |
| GET | `/api/reports/statistics/summary` | Get report statistics |

### Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | Get user notifications |
| GET | `/api/notifications/unread-count` | Get unread count |
| POST | `/api/notifications/{id}/mark-read` | Mark as read |
| POST | `/api/notifications/mark-all-read` | Mark all as read |
| POST | `/api/notifications/` | Create notification |

## Data Migration

### From Flutter App

1. **Export data from Flutter app** (this needs to be implemented in Flutter):
   ```dart
   // In Flutter app, create export function
   Future<void> exportToJson() async {
     final data = {
       'reports': await DatabaseService.instance.getAllReports(),
       'users': await DatabaseService.instance.getAllUsers(),
       'notifications': await DatabaseService.instance.getNotifications(),
       // ... other data
     };
     
     // Save to file or send to backend
   }
   ```

2. **Run migration script:**
   ```bash
   python utils/data_migration.py path/to/flutter_export.json
   ```

### Database Reset

⚠️ **WARNING: This deletes all data!**

```bash
python utils/db_init.py reset
```

## Configuration

### Environment Variables (.env)

```env
# Server
PORT=8000
DATABASE_URL=sqlite:///./civic_welfare.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
FLUTTER_WEB_ORIGIN=http://localhost:3000
FLUTTER_MOBILE_ORIGIN=http://10.0.2.2:8000

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

## Database Schema

### Core Tables

- **users** - User accounts (public, officer, admin)
- **reports** - Civic issue reports
- **notifications** - System notifications
- **registration_requests** - Pending user registrations
- **password_reset_requests** - Password reset requests
- **report_updates** - Report status updates/comments
- **sessions** - User sessions (for advanced auth)

### Relationships

```
User 1:N Report (as reporter)
User 1:N Report (as assigned officer)
Report 1:N ReportUpdate
Report 1:N Notification
User 1:N Notification
```

## API Examples

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "citizen@civicwelfare.com",
    "password": "citizen123"
  }'
```

### Create Report

```bash
curl -X POST "http://localhost:8000/api/reports/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Broken Street Light",
    "description": "Street light on Main St is not working",
    "category": "Infrastructure",
    "location": "Main Street, Downtown",
    "priority": "medium",
    "department": "streetLights"
  }'
```

### Get Reports

```bash
curl -X GET "http://localhost:8000/api/reports/" \
  -H "Authorization: Bearer <token>"
```

## Development

### Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration
├── database/
│   ├── database.py        # Database connection
│   ├── models.py          # SQLAlchemy models
│   └── __init__.py
├── api/
│   ├── routes/
│   │   ├── auth.py        # Authentication routes
│   │   ├── users.py       # User management routes
│   │   ├── reports.py     # Report routes
│   │   ├── notifications.py # Notification routes
│   │   └── __init__.py
│   ├── middleware.py      # FastAPI middleware
│   └── __init__.py
└── utils/
    ├── auth.py            # Authentication utilities
    ├── db_init.py         # Database initialization
    ├── data_migration.py  # Data migration utilities
    └── __init__.py
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Adding New Features

1. **Add database model** in `database/models.py`
2. **Create migration** if needed
3. **Add API routes** in `api/routes/`
4. **Update authentication** if required
5. **Add tests**

## Production Deployment

### Security Considerations

1. **Change default passwords**
2. **Use strong SECRET_KEY**
3. **Configure proper CORS origins**
4. **Use HTTPS in production**
5. **Set up proper logging**
6. **Use environment-specific configuration**

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the backend directory and dependencies are installed
2. **Database locked**: Close any other applications using the SQLite file
3. **Permission errors**: Check file permissions on the database file
4. **Port already in use**: Change PORT in .env or kill the process using port 8000

### Logs

The application logs important information to the console. For production, configure proper logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the Civic Welfare Management System and follows the same license terms.