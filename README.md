# Django Blog

A clean, responsive Django blog with user authentication, profiles, post likes, and comment likes (Instagram‑style).

## Features
- User registration, login, logout
- Profile page with avatar
- Public profile view
- Create, edit, delete posts
- Like posts
- Comment system
- Like comments
- Clean UI with Bootstrap

## Tech Stack
- Python
- Django
- SQLite (local development)
- Bootstrap 5

## Setup Instructions

### 1) Clone the repo
```bash
git clone <your-repo-url>
cd django_project
```

### 2) Create virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5) Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 6) Run server
```bash
python manage.py runserver
```

Open in browser:
```
http://127.0.0.1:8000
```

---

## Notes
- Database (`db.sqlite3`) and user uploads (`media/`) are excluded from GitHub.
- You can create demo content locally after running migrations.

---

---

## Author
Created by **Aaditya karn**