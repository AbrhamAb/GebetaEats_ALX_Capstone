# GebetaEats (Simple Food Delivery)

This repository contains a simple, beginner-friendly food delivery web application built with Django, Django REST Framework (DRF), and Django templates. It demonstrates core concepts: authentication, REST APIs, image uploads, session cart, orders, and a minimal Bootstrap-based frontend.

Technology stack
- Django (backend + templates)
- Django REST Framework (APIs)
- SQLite (development database)
- Bootstrap (CSS via CDN)
- Pillow (image uploads)

Quick start (development)
1) Create & activate a virtualenv and install dependencies:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Create migrations and migrate the database:
```powershell
python manage.py makemigrations
python manage.py migrate
```

3) Create a superuser to access the admin panel:
```powershell
python manage.py createsuperuser
```

4) Run the development server:
```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view the site. Admin: http://127.0.0.1:8000/admin/

Project layout (important files)
- `accounts/` — custom `User` model with `role` (customer or restaurant), admin, serializers, and registration form.
- `restaurants/` — `Restaurant` model, admin, API serializers/views.
- `menu/` — `Category` and `MenuItem` (with image upload), admin, API.
- `orders/` — `Order` and `OrderItem` models, serializers, API and admin.
- `web/` — template views: home, restaurant detail, cart, checkout, registration/login.
- `api/` — DRF viewsets and router for API endpoints.

Core features implemented
- User registration and login (template views + API register endpoint).
- Customer and Restaurant roles (users select role during signup).
- Restaurants create profiles and manage menu items (via admin or API).
- Menu items support image uploads (requires Pillow).
- Session-based cart (add/update/remove items) and checkout creating orders.
- Order lifecycle: Pending → Preparing → Out for delivery → Delivered (restaurant can update status).
- REST APIs (viewsets) for restaurants, menu items, categories, and orders (JWT available).

API examples (JWT)
1) Obtain tokens:
```bash
POST /api/auth/token/  {"username": "user", "password": "pass"}
```

2) Use `Authorization: Bearer <access_token>` header to call protected endpoints.

Available API endpoints
- `GET /api/restaurants/` — list restaurants
- `GET /api/items/` — list menu items
- `GET /api/categories/` — list categories
- `GET /api/orders/` — user orders (restaurant owners see orders for their restaurant)
- Refer to DRF router at `/api/` for full routes.

Notes & next steps
- Remember to install `Pillow` to support image uploads.
- For production, set `DEBUG = False`, configure `ALLOWED_HOSTS`, static/media hosting, and secure secret settings.
- This project is intentionally simple for learning. Improvements: add pagination, search filters, image validations, unit tests, and richer permissions.

If you'd like, I can now:
- run migrations and create a superuser here,
- or continue by adding tests and API documentation examples.
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
- `POST /api/auth/logout/` – logout (client-side token discard)

- `GET /api/vendors/` – list vendors
- `POST /api/vendors/` – vendor users create their vendor profile
- `GET /api/vendors/<id>/` – vendor detail
- `GET/PATCH /api/vendors/me/` – get or update your vendor profile (vendor role required)

- `GET /api/vendors/<vendor_id>/menu/` – menu items for a vendor
- `POST /api/vendors/<vendor_id>/menu/` – vendor create menu item (vendor role required)
- `GET/PATCH/DELETE /api/vendors/<vendor_id>/menu/<id>/` – vendor item CRUD (owner only)

- `GET /api/vendors/menu-items/` – global catalog list (filters: vendor, category, available, min_price, max_price)
- `GET /api/vendors/menu-items/<id>/` – global menu item detail

- `POST /api/orders/` – create order (authenticated customers only)
- `GET /api/orders/` – user order history
- `GET /api/orders/<id>/` – order detail (owner or vendor)
- `POST /api/orders/<id>/cancel/` – cancel an order (allowed states only)

- `GET /api/orders/vendor/` – vendor incoming orders
- `PATCH /api/orders/<id>/status/` – vendor update order status (allowed transitions enforced)

- `PATCH /api/orders/delivery/<id>/assign/` – vendor assign a rider to a delivery
- `PATCH /api/orders/delivery/<id>/status/` – rider update delivery status (assigned rider only)
- `GET /api/orders/delivery/assigned/` – rider list of assigned deliveries

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
