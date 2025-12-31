# Django Tutorial (Quickstart)

## Prerequisites
- Python 3.10+ installed (`python --version`)
- pip available (`python -m pip --version`)
- (Optional) VS Code + Python extension

## 1) Create & activate a virtual environment
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

## 2) Install Django
```bash
pip install "django>=5.0,<6.0"
pip freeze > requirements.txt
```

## 3) Start a project
```bash
django-admin startproject config .
```
This creates:
```
config/
  __init__.py
  settings.py
  urls.py
  asgi.py
  wsgi.py
manage.py
```

## 4) Run initial checks
```bash
python manage.py migrate
python manage.py runserver 8000
# Visit http://127.0.0.1:8000
```

## 5) Create an app
```bash
python manage.py startapp core
```
Add the app to `config/settings.py`:
```python
INSTALLED_APPS = [
    # ...
    "core",
]
```

## 6) Minimal view, URL, and template
`core/views.py`
```python
from django.shortcuts import render

def home(request):
    return render(request, "home.html", {"message": "Hello Django!"})
```

`config/urls.py`
```python
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
]
```

Create template directory and file:
```bash
mkdir -p templates
```
`templates/home.html`
```html
<!DOCTYPE html>
<html lang="en">
  <head><meta charset="utf-8"><title>Home</title></head>
  <body>
    <h1>{{ message }}</h1>
  </body>
</html>
```
Point Django to the templates folder in `config/settings.py`:
```python
TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]
```

## 7) Models, migrations, admin (example)
`core/models.py`
```python
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```
Run migrations and register in admin:
```bash
python manage.py makemigrations
python manage.py migrate
```
`core/admin.py`
```python
from django.contrib import admin
from .models import Note

admin.site.register(Note)
```

## 8) Basic tests (example)
`core/tests.py`
```python
from django.test import Client, TestCase
from django.urls import reverse

class HomeViewTests(TestCase):
    def test_home_renders(self):
        c = Client()
        resp = c.get(reverse("home"))
        self.assertContains(resp, "Hello Django!")
```
Run tests:
```bash
python manage.py test
```

## 9) Static files (optional)
In `config/settings.py`:
```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```
Create a `static/` folder for CSS/JS/images.

## 10) Next steps
- Add forms/views for `Note` CRUD.
- Configure environment variables for secrets (`SECRET_KEY`, DB settings).
- Add `.env` handling with `python-dotenv` or `environs` if needed.
- Use `collectstatic` for deployments.

Happy coding!
