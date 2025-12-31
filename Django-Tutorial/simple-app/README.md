# Django Simple App

A minimal Django application demonstrating basic concepts including views, models, templates, and admin interface.

## Project Structure

```
simple-app/
├── config/              # Project configuration
│   ├── settings.py      # Django settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI config
│   └── asgi.py          # ASGI config
├── core/                # Main application
│   ├── models.py        # Note model
│   ├── views.py         # Home view
│   ├── admin.py         # Admin configuration
│   ├── tests.py         # Unit tests
│   └── apps.py          # App configuration
├── templates/           # HTML templates
│   └── home.html        # Home page template
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Quick Start

### 1. Create and activate virtual environment

**Windows PowerShell:**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 5. Run development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 to see the app!

## Features

- **Home Page**: Simple landing page with styled template
- **Note Model**: Example model with CRUD operations
- **Admin Interface**: Visit http://127.0.0.1:8000/admin
- **Unit Tests**: Run with `python manage.py test`

## Running Tests

```bash
python manage.py test
```

## Admin Interface

After creating a superuser, you can:
1. Visit http://127.0.0.1:8000/admin
2. Login with your credentials
3. Manage Notes through the admin panel

## Next Steps

- Add more views and URLs
- Create forms for Note creation/editing
- Add API endpoints with Django REST Framework
- Implement user authentication
- Add more models and relationships
- Deploy to production (Heroku, Railway, etc.)

## Technologies

- Django 5.0+
- SQLite (default database)
- Python 3.10+

## Notes

- `SECRET_KEY` is set to a development value. Change it for production!
- `DEBUG = True` should be `False` in production
- SQLite database is used by default (suitable for development)
