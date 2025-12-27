GebetaEats – Capstone Part 4 Progress Update

1) What I accomplished this week

- Expanded backend beyond auth/vendors/menu to include orders and deliveries.
- Order flow: customers can place orders (single-vendor), view their history, cancel pending/accepted; vendors can view their orders and update status; riders can see assigned deliveries and update status.
- Delivery flow: vendors assign riders; riders update delivery status (picked/delivered/failed) with timestamps.
- Menu/catalog: added global menu listing with filters (vendor, category, availability, price) plus per-vendor CRUD retained.
- Auth: kept JWT login/register/me and added a logout endpoint (client-side token discard).
- Roles/permissions: tightened with customer/vendor/rider checks and ownership validation.
- Updated models to match design doc: delivery address, total_price, unit/line totals, expanded order/delivery statuses.

2) Challenges and how I handled them

- Schema alignment vs. earlier code: The order/delivery models needed renaming and extra fields (delivery_address, total_price, timestamps). I revised models/serializers/views together to keep API responses consistent.
- Role-based access: Ensuring vendors can only mutate their own menu items/orders and riders only their assigned deliveries. Added ownership checks and custom permissions.
- Status handling: Added clear status enums for orders and deliveries; added validation on vendor status updates and rider updates to avoid invalid transitions.

3) What’s next (upcoming week)

- Add stricter status transition rules (e.g., pending → accepted → preparing → out_for_delivery → delivered; allow cancel only in early states).
- Vendor self-onboarding endpoint (optional) and richer vendor profile fields if needed.
- Improve docs/README with all current endpoints and sample requests.
- Add automated tests for auth, vendor menu CRUD, order create/cancel, vendor status updates, and rider delivery updates.
- Optional: Server-side cart endpoints if time permits.

Repo link

- GitHub (public): https://github.com/AbrhamAb/GebetaEats_ALX_Capstone

Endpoints implemented (snapshot)

- Auth: POST /api/auth/register/, POST /api/auth/login/, GET /api/auth/me/, POST /api/auth/logout/
- Vendors: GET /api/vendors/, GET /api/vendors/<id>/, GET/PATCH /api/vendors/me/
- Menu (vendor-scoped): GET/POST /api/vendors/<vendor_id>/menu/, GET/PATCH/DELETE /api/vendors/<vendor_id>/menu/<id>/
- Menu catalog: GET /api/vendors/menu-items/, GET /api/vendors/menu-items/<id>/ with filters vendor, category, available, min_price, max_price
- Orders (customer): GET/POST /api/orders/, GET /api/orders/<id>/, POST /api/orders/<id>/cancel/
- Orders (vendor): GET /api/orders/vendor/, PATCH /api/orders/<id>/status/
- Delivery (vendor/rider): PATCH /api/orders/delivery/<id>/assign/, PATCH /api/orders/delivery/<id>/status/, GET /api/orders/delivery/assigned/

Notes

- After pulling changes, run migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

- Run server:

```powershell
python manage.py runserver
```
