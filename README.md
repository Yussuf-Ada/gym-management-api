# Gym Management API

A comprehensive Django REST API for gym management with enterprise-grade authentication, cloud integrations, and full testing coverage.

## 🏋️ Overview

This API provides a complete backend solution for gym management, including member management, class bookings, membership subscriptions, and administrative features.

## 🚀 Features

- **Enterprise Authentication**: JWT-based authentication with password reset
- **Member Management**: Complete CRUD operations for gym members
- **Class Booking System**: Schedule and manage gym classes
- **Membership Subscriptions**: Flexible membership plans and billing
- **Cloud Integrations**: SendGrid emails and Cloudinary image storage
- **Comprehensive Testing**: 68% test coverage with 25 tests
- **Enterprise Security**: CORS, authentication, and data validation

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 12+ (for production) / SQLite (for development)
- SendGrid account (for emails)
- Cloudinary account (for image storage)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Yussuf-Ada/gym-management-api.git
cd gym-management-api
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file with the following variables:

```bash
# Database Configuration
DATABASE_URL=postgres://username:password@localhost:5432/gymdb

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# SendGrid Configuration
SENDGRID_API_KEY=SG.your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourgym.com

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Load Mock Data (Optional)
```bash
python manage.py setup_mock_data
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api`

## 🏗️ Architecture

### Project Structure
```
gym-management-api/
├── gym_management/          # Django settings and configuration
├── users/                   # Authentication and user management
├── members/                 # Member management
├── memberships/             # Membership subscriptions
├── classes/                 # Gym classes and bookings
├── requirements.txt         # Python dependencies
└── manage.py              # Django management script
```

### Key Components

#### Authentication System
- JWT token-based authentication
- Password reset with email verification
- User profile management
- Role-based access control

#### API Endpoints
- `/api/auth/` - Authentication endpoints
- `/api/members/` - Member management
- `/api/memberships/` - Subscription management
- `/api/classes/` - Class scheduling
- `/api/dashboard/` - Administrative statistics

#### Cloud Integrations
- **SendGrid**: Password reset emails and notifications
- **Cloudinary**: Profile image storage and optimisation

## 🔐 Authentication

### Login
```bash
POST /api/auth/login/
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Registration
```bash
POST /api/auth/register/
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Password Reset
```bash
POST /api/auth/password-reset/
{
  "email": "user@example.com"
}
```

## 🧪 Testing

### Run All Tests
```bash
python manage.py test users.tests members.tests users.test_dashboard memberships.test_crud
```

### Run Tests with Coverage
```bash
coverage run --source='.' manage.py test users.tests members.tests users.test_dashboard memberships.test_crud
coverage report
```

### Test Coverage
- **Total Coverage**: 68%
- **Tests**: 25 comprehensive tests
- **Coverage Areas**: Authentication, CRUD operations, API endpoints, security

## 🚀 Deployment

### Environment Variables for Production
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-production-database-url
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Deployment Steps
1. Set up PostgreSQL database
2. Configure environment variables
3. Install dependencies
4. Run migrations
5. Collect static files
6. Configure web server (Gunicorn + Nginx)
7. Set up SSL certificate

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset/confirm/` - Confirm password reset
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/` - Update user profile

### Member Endpoints
- `GET /api/members/` - List all members
- `POST /api/members/` - Create new member
- `GET /api/members/{id}/` - Get member details
- `PATCH /api/members/{id}/` - Update member
- `DELETE /api/members/{id}/` - Delete member

### Membership Endpoints
- `GET /api/memberships/` - List all memberships
- `POST /api/memberships/` - Create membership
- `GET /api/memberships/{id}/` - Get membership details
- `PATCH /api/memberships/{id}/` - Update membership
- `DELETE /api/memberships/{id}/` - Delete membership

### Class Endpoints
- `GET /api/classes/` - List all classes
- `POST /api/classes/` - Create new class
- `GET /api/classes/{id}/` - Get class details
- `PATCH /api/classes/{id}/` - Update class
- `DELETE /api/classes/{id}/` - Delete class

### Dashboard Endpoints
- `GET /api/dashboard/stats/` - Get dashboard statistics

## 🔧 Technical Decisions

### Framework Choice
- **Django REST Framework**: Chosen for its robust authentication, serializers, and enterprise features
- **PostgreSQL**: Selected for reliability and advanced features
- **JWT Authentication**: Provides stateless, scalable authentication

### Cloud Services
- **SendGrid**: Enterprise-grade email delivery with tracking
- **Cloudinary**: Optimised image storage and CDN delivery
- **Render**: Simplified deployment with automatic scaling

### Security Measures
- CORS configuration for cross-origin requests
- JWT token expiration and refresh
- Password validation and hashing
- Input sanitisation and validation

### Testing Strategy
- Unit tests for business logic
- Integration tests for API endpoints
- Authentication and security testing
- 68% code coverage target

## 📞 Support

For support and queries, please create an issue on GitHub: [Create an issue](https://github.com/Yussuf-Ada/gym-management-api/issues)

## 🌐 Live Deployment

- **API**: https://gym-management-api-me3d.onrender.com
- **Frontend**: https://gym-management-frontend-zeta.vercel.app

## 🤖 AI Usage

This project was developed with assistance from generative AI tools to support learning and development. All code and implementations have been thoroughly reviewed and are fully understood.

**AI tools were used for:**
- **Code Structure**: Project scaffolding and component organisation
- **Debugging Support**: Resolving issues with SendGrid, Cloudinary, and testing
- **Architecture Guidance**: Django REST Framework best practices and security
- **Testing Strategy**: Developing comprehensive test cases and achieving 80% coverage
- **Documentation**: Improving technical documentation clarity

---
