# GebetaEats Backend

Django REST API for the GebetaEats food and essentials delivery platform. Part 3 focuses on getting core pieces working: auth, vendor listing, and vendor menus.

## Quick start

1) Create and activate a virtualenv, then install dependencies:
```bash
pip install -r requirements.txt
```

2) Run migrations and start the dev server:
```bash
python manage.py migrate
python manage.py runserver
```

## Core endpoints (Week 1)

- `POST /api/auth/register/` – create account
- `POST /api/auth/login/` – get JWT access/refresh tokens
- `GET /api/auth/me/` – current user profile
- `GET /api/vendors/` – list vendors
- `GET /api/vendors/<id>/` – vendor detail
- `GET /api/vendors/<vendor_id>/menu/` – menu items for a vendor

## Project structure
```
gebetaeats_backend/
├── manage.py
├── gebetaeats_backend/   # project settings and root urls
├── users/                # custom user model + auth endpoints
├── vendors/              # vendor profile models and listing
├── menu/                 # categories and menu items
└── requirements.txt
```
