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
