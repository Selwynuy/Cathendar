# Cathendar - Calendar Web Application

A beautifully designed collaborative calendar web application built with Django. Share calendars with friends, mark availability, and see everyone's schedules in one unified view. Features include public holidays integration, real-time collaboration, and a custom admin panel.

## 🌟 Features

### Core Functionality
- **Calendar Management**: Create and manage multiple calendars with a beautiful centered UI
- **Event Management**: Add, edit, and delete events with titles and descriptions
- **Availability Marking**: Mark dates as busy or available with optional notes
- **Calendar Sharing**: Share calendars with other users for collaboration
- **Merged View**: See events and availability from all your calendars in one unified view
- **Public Holidays**: Automatic display of public holidays (supports multiple countries)

### User Features
- **Username-based Authentication**: Login with username (not email)
- **Auto-calendar Creation**: Default calendar created automatically on registration
- **Shared Calendar Creation**: Create shared calendars directly when sharing with users
- **Event Details**: Click events to view full details in a modal
- **Availability Details**: Click availability markers to see user status and notes

### Admin Panel
- **Custom Admin Interface**: Separate from Django's default admin
- **Full CRUD Operations**: Manage users, calendars, and events
- **Analytics Dashboard**: View statistics and insights
- **Staff-only Access**: Secure admin panel for staff members

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (Python 3.10+ recommended)
- **pip** (Python package manager)
- **Redis** (for Channels and Celery - optional for basic functionality)
- **PostgreSQL** (optional, SQLite is used by default for development)

### Installing Redis (Optional)

**Windows:**
- Download from [Redis for Windows](https://github.com/microsoftarchive/redis/releases) or use WSL
- Or use Docker: `docker run -d -p 6379:6379 redis`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

**macOS:**
```bash
brew install redis
brew services start redis
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Cathendar
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv

# Linux/macOS
python3 -m venv venv
```

### 3. Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.0+
- Django REST Framework
- Django Channels (for WebSocket support)
- Celery (for background tasks)
- Redis client
- JWT authentication
- Holidays library (for public holidays)
- And other dependencies

### 5. Environment Variables

Create a `.env` file in the project root (optional, defaults are provided):

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - SQLite used by default)
# DATABASE_URL=postgresql://user:password@localhost:5432/cathendar

# Redis (optional - for Channels/Celery)
# REDIS_URL=redis://localhost:6379/0
```

**Note**: For production, generate a secure SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Database Setup

#### Run Migrations

```bash
python manage.py migrate
```

This creates all necessary database tables:
- Users (custom user model)
- Calendars
- Events
- Availability
- Friends
- Calendar Shares
- Holidays

#### Create Database Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

#### Create Staff User (for Custom Admin Panel)

You can either:
1. Use Django admin to set `is_staff=True` for a user
2. Or use the provided script:

```bash
python make_staff.py
```

This will prompt you to enter a username and grant staff privileges.

### 7. Populate Public Holidays

Populate holidays for your country:

```bash
# For a specific country and year
python manage.py populate_holidays --country US --year 2024

# For multiple years
python manage.py populate_holidays --country US --years 2024 2026

# For current and next year (default)
python manage.py populate_holidays --country US
```

**Supported Countries**: US, GB, CA, AU, DE, FR, and many more. See the [holidays library documentation](https://github.com/vacanza/python-holidays) for full list.

**Examples:**
```bash
# United States
python manage.py populate_holidays --country US --years 2024 2026

# United Kingdom
python manage.py populate_holidays --country GB --years 2024 2026

# Canada
python manage.py populate_holidays --country CA --years 2024 2026
```

### 8. Collect Static Files (Production)

```bash
python manage.py collectstatic
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The application will be available at:
- **Main Calendar App**: http://127.0.0.1:8000/
- **Custom Admin Panel**: http://127.0.0.1:8000/admin-panel/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **API Base**: http://127.0.0.1:8000/api/

## 📁 Project Structure

```
Cathendar/
├── admin_panel/          # Custom admin panel app
│   ├── views.py         # Admin views
│   ├── urls.py          # Admin URLs
│   └── templates/       # Admin templates
├── calendar_app/        # Main calendar application
│   ├── views.py         # Calendar views
│   ├── urls.py          # Calendar URLs
│   └── templates/       # Calendar templates
├── core/                # Core app with models and API
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── admin_views.py   # Admin API views
│   ├── permissions.py   # Custom permissions
│   ├── management/
│   │   └── commands/
│   │       └── populate_holidays.py  # Holiday population command
│   └── migrations/      # Database migrations
├── cathendar/           # Django project settings
│   ├── settings.py      # Project settings
│   ├── urls.py         # Root URL configuration
│   ├── wsgi.py         # WSGI config
│   └── asgi.py         # ASGI config (for Channels)
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── requirements.txt     # Python dependencies
├── manage.py           # Django management script
└── .env                # Environment variables (create this)
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/refresh/` - Refresh JWT token

### Calendars
- `GET /api/calendars/` - List user's calendars (owned + shared)
- `POST /api/calendars/` - Create calendar
- `GET /api/calendars/{id}/` - Get calendar details
- `PUT /api/calendars/{id}/` - Update calendar
- `DELETE /api/calendars/{id}/` - Delete calendar (owner only)
- `POST /api/calendars/create_shared/` - Create shared calendar with user
- `GET /api/calendars/{id}/shared_with/` - List users calendar is shared with

### Events
- `GET /api/events/` - List events (filter by `?calendar_id={id}`)
- `POST /api/events/` - Create event
- `GET /api/events/{id}/` - Get event details
- `PUT /api/events/{id}/` - Update event
- `DELETE /api/events/{id}/` - Delete event

### Availability
- `GET /api/availability/` - List availability (filter by `?calendar_id={id}`)
- `POST /api/availability/` - Mark availability (busy/available)
- `GET /api/availability/{id}/` - Get availability details
- `PUT /api/availability/{id}/` - Update availability
- `DELETE /api/availability/{id}/` - Remove availability
- `GET /api/availability/aggregated/?calendar_id={id}` - Get all users' availability for calendar

### Holidays
- `GET /api/holidays/` - List holidays (filter by `?country={code}&year={year}`)
- `GET /api/holidays/for_date_range/?country={code}&start_date={date}&end_date={date}` - Get holidays for date range

### Users
- `GET /api/users/` - List users
- `GET /api/users/me/` - Get current user

### Admin API
- `GET /api/admin/users/` - List all users (staff only)
- `GET /api/admin/calendars/` - List all calendars (staff only)
- `GET /api/admin/events/` - List all events (staff only)
- `GET /api/admin/analytics/dashboard/` - Get analytics (staff only)

**Note**: All API endpoints require authentication (JWT token or session). Admin endpoints require staff privileges.

## 🛠️ Management Commands

### Populate Holidays

```bash
python manage.py populate_holidays [options]
```

**Options:**
- `--country CODE`: ISO country code (default: US)
- `--year YEAR`: Single year to populate
- `--years START END`: Range of years (e.g., `--years 2024 2026`)
- `--clear`: Clear existing holidays for country before populating

**Examples:**
```bash
# Populate US holidays for 2024-2026
python manage.py populate_holidays --country US --years 2024 2026

# Populate UK holidays for current year
python manage.py populate_holidays --country GB

# Clear and repopulate
python manage.py populate_holidays --country US --years 2024 2026 --clear
```

### Other Django Commands

```bash
# Create superuser
python manage.py createsuperuser

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Django shell
python manage.py shell
```

## 🔐 Authentication

### User Registration
Users can register through the web interface at `/login/` or via API:
```bash
POST /api/auth/register/
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "password_confirm": "securepassword"
}
```

### User Login
Login is username-based (not email). Users can login through:
- Web interface at `/login/`
- API endpoint: `POST /api/auth/login/`

### Admin Panel Access
Access the custom admin panel at `/admin-panel/` with a staff account.

## 🗄️ Database Models

- **User**: Custom user model (username-based authentication)
- **Calendar**: User calendars with name and description
- **Event**: Calendar events with title, description, and time range
- **Availability**: User availability markers (busy/available) with optional title/description
- **Friend**: Friend relationships between users
- **CalendarShare**: Calendar sharing permissions (view_only, edit, admin)
- **Holiday**: Public holidays with date, name, country, and description

## 🎨 Frontend

The application uses:
- **Django Templates** for server-side rendering
- **Font Awesome** for icons
- **Vanilla JavaScript** for interactivity
- **CSS3** with modern styling
- **Modal System** for notifications and confirmations

## 🔧 Configuration

### Settings File
Main configuration is in `cathendar/settings.py`. Key settings:

- `AUTH_USER_MODEL = 'core.User'` - Custom user model
- `LOGIN_URL = '/login/'` - Login redirect
- `REST_FRAMEWORK` - DRF configuration
- `CHANNEL_LAYERS` - Channels/Redis configuration
- `SIMPLE_JWT` - JWT token settings

### Environment Variables
Use `.env` file for:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated host list

## 🚀 Production Deployment

### Before Deploying

1. **Set DEBUG=False** in `.env` or settings
2. **Generate new SECRET_KEY**:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
3. **Update ALLOWED_HOSTS** with your domain
4. **Use PostgreSQL** instead of SQLite
5. **Set up Redis** for Channels/Celery
6. **Collect static files**: `python manage.py collectstatic`
7. **Set up proper WSGI server** (Gunicorn, uWSGI)
8. **Configure reverse proxy** (Nginx, Apache)
9. **Set up SSL/HTTPS**

### Database Migration in Production

```bash
python manage.py migrate
```

### Static Files

```bash
python manage.py collectstatic --noinput
```

## 🧪 Development

### Running Tests

```bash
python manage.py test
```

### Code Style

Follow PEP 8 Python style guide. Consider using:
- `black` for code formatting
- `flake8` for linting
- `pylint` for code analysis

## 📝 Additional Documentation

- `PROJECT_PLAN.md` - Project architecture and planning
- `API_INTEGRATIONS.md` - External API integration plans
- `ADMIN_PANEL.md` - Admin panel documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

[Add your license here]

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'holidays'`
**Solution**: Run `pip install -r requirements.txt`

**Issue**: `django.db.utils.OperationalError: no such table`
**Solution**: Run `python manage.py migrate`

**Issue**: Cannot access admin panel
**Solution**: Ensure user has `is_staff=True`. Use `python make_staff.py` or Django admin.

**Issue**: Holidays not showing
**Solution**: Run `python manage.py populate_holidays --country US --years 2024 2026`

**Issue**: Redis connection error (Channels)
**Solution**: Ensure Redis is running or remove Channels from INSTALLED_APPS if not needed.

## 📞 Support

For issues and questions, please open an issue on the repository.

---

**Built with ❤️ using Django**
