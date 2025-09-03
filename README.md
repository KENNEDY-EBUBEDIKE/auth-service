# Auth Service - Django Authentication System

A Django-based user authentication system with JWT tokens, PostgreSQL database, Redis caching, and password reset functionality.

## Features

- User registration with email as username
- JWT-based authentication
- Password reset with Redis-cached tokens
- PostgreSQL database integration
- Redis caching
- Rate limiting on login and password reset
- Swagger API documentation
- Docker support
- Unit tests

## Project Structure

```
auth_service/
├── auth_service/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── apps.py
│   ├── admin.py
│   └── tests.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── railway.toml
├── render.yaml
└── README.md
```

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd auth_service
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000/api/auth/
   - Swagger Documentation: http://localhost:8000/swagger/
   - Admin Panel: http://localhost:8000/admin/
   - Railway App URL: https://auth-service-production-6598.up.railway.app/

## Environment Variables

| Variable | Description | Example                                  |
|----------|-------------|------------------------------------------|
| `DEBUG` | Debug mode (True/False) | `True`                                   |
| `SECRET_KEY` | Django secret key | `your-secret-key-here`                   |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:port/db`    |
| `REDIS_URL` | Redis connection string | `redis://host:port/db`                   |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1,railway-domain.com` |

## API Endpoints

### Authentication

#### Register User
- **URL**: `POST /api/auth/register/`
- **Body**:
  ```json
  {
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
  }
  ```

#### Login
- **URL**: `POST /api/auth/login/`
- **Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "email": "john@example.com",
      "full_name": "John Doe"
    }
  }
  ```

#### Refresh Token
- **URL**: `POST /api/auth/token/refresh/`
- **Body**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### Forgot Password
- **URL**: `POST /api/auth/forgot-password/`
- **Body**:
  ```json
  {
    "email": "john@example.com"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Password reset token sent to your email",
    "token": "abc123..." 
  }
  ```

#### Reset Password
- **URL**: `POST /api/auth/reset-password/`
- **Body**:
  ```json
  {
    "token": "abc123...",
    "new_password": "NewSecurePassword123!",
    "new_password_confirm": "NewSecurePassword123!"
  }
  ```

#### User Profile
- **URL**: `GET /api/auth/profile/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "id": 1,
    "email": "john@example.com",
    "full_name": "John Doe",
    "date_joined": "2025-01-01T00:00:00Z",
    "is_active": true
  }
  ```

## Local Development (without Docker)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL and Redis**
   ```bash
   # Start PostgreSQL and Redis services
   # Update .env with your local database credentials
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

## Testing

Run the test suite:
```bash
python manage.py test
```

Run tests with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Security Features

- **Rate Limiting**: Login (5/minute) and password reset (3/minute) endpoints are rate-limited by IP
- **JWT Authentication**: Secure token-based authentication
- **Password Validation**: Django's built-in password validators
- **Token Expiry**: Password reset tokens expire after 10 minutes
- **CORS Support**: Configurable cross-origin resource sharing

## Monitoring and Health Checks

- Health check endpoint: `/swagger/` (shows API documentation)
- Admin panel: `/admin/`
- API documentation: `/swagger/` and `/redoc/`

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in environment variables
   - Verify database credentials

2. **Redis Connection Error**
   - Ensure Redis is running
   - Check REDIS_URL in environment variables
   - Verify Redis service is accessible

3. **Migration Issues**
   - Run `python manage.py makemigrations accounts`
   - Run `python manage.py migrate`

### Docker Issues

1. **Port already in use**
   ```bash
   docker-compose down
   # Change ports in docker-compose.yml if needed
   ```

2. **Permission denied**
   ```bash
   sudo docker-compose up --build
   ```

