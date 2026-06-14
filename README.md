# OTP Authentication API

REST API for user registration and authentication with email OTP verification using Django, Redis, and Celery.

## 🛠 Tech Stack

- Django 6.0.6 + Django REST Framework
- Redis (caching, sessions, message broker)
- Celery (async tasks)
- SQLite (development)
- SMTP email integration

## 📁 Project Structure

```
src/apps/users/
├── api/
│   └── views/          # Separate views for each endpoint
│       ├── register.py
│       ├── verify.py
│       ├── login.py
│       ├── logout.py
│       └── resend_otp.py
├── utils/
│   ├── otp.py         # OTP generation & validation
│   └── email.py       # Email sending
├── serializer/        # Data validation
├── models.py
├── tasks.py           # Celery async tasks
└── admin.py           # Django admin config
```

## � API Endpoints

### 1. Register
```
POST /api/register/
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "password123"
}
```
- Validates input
- Generates OTP
- Sends OTP via email
- Stores user data in Redis (10 min expiry)
- User not created until verified

### 2. Verify OTP
```
POST /api/verify/
{
  "email": "user@example.com",
  "otp": "1234"
}
```
- Validates OTP
- Creates user in database
- Cleans up temporary data

### 3. Login
```
POST /api/login/
{
  "email": "user@example.com",
  "password": "password123"
}
```
- Validates credentials
- Creates session

### 4. Logout
```
POST /api/logout/
```

### 5. Resend OTP
```
POST /api/resend-otp/
{
  "email": "user@example.com"
}
```
- Rate limited (3 attempts per 5 min)

## 🗄️ Data Model

```python
class User(models.Model):
    id          (auto)
    name        CharField(max_length=255)
    email       EmailField(unique=True)
    password    CharField(max_length=255)
    tg_id       CharField(nullable=True)
```

## 🔐 Key Implementation Details

- **Password Security**: Passwords hashed using Django's `make_password()`
- **OTP Expiration**: 2 minutes, stored in Redis
- **Session Storage**: Redis-backed sessions
- **Email Delivery**: Asynchronous via Celery
- **Rate Limiting**: Max 3 OTP resends per 5 minutes
- **Validation**: Input validation on all endpoints
- **Error Handling**: Comprehensive error responses with status codes

## 🚀 Installation

```bash
git clone <repo>
cd OTP-Authentication-API

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add EMAIL_HOST_USER and EMAIL_HOST_PASSWORD

# Start Redis
redis-server

# Run migrations
python3 manage.py migrate

# Start server
python3 manage.py runserver
```

## ⚙️ Configuration

Create `.env` file:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Redis configuration in `config/settings.py`:
- Cache: `redis://127.0.0.1:6379/1`
- Celery: `redis://127.0.0.1:6379/0`
- Sessions: Redis-backed

## 📝 Django Admin

Customized admin interface at `/admin/users/user/`:
- List view with email, name, telegram ID
- Searchable by name, email, telegram ID
- Grouped fieldsets (Personal, Security, Telegram)
- Password field collapsible

## � Authentication Flow

```
Register → OTP Sent → Verify OTP → User Created → Login → Session
```

1. User registers with email and password
2. OTP generated and sent via email
3. User verifies OTP
4. User created in database only after successful verification
5. User logs in with email and password
6. Session stored in Redis
