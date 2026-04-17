# Ecommerce Website (Django)

A Django-based ecommerce app with:
- Customer-facing catalog, cart, and order flow
- Admin product/category management
- Cash on Delivery and eSewa payment paths
- Profile management and authentication

## Tech Stack
- Python 3.9+
- Django 5.0.1
- MySQL (optional) or SQLite (default)
- Crispy Forms + Bootstrap 4

## Project Structure
- `ecommerce/` - Django project config (`settings.py`, root URLs)
- `userspage/` - customer pages, auth, cart/order/payment views
- `product/` - product/category models, forms, admin CRUD views
- `adminpage/` - custom admin dashboard UI
- `templates/` - shared base template
- `static/` - CSS/JS/images and seeded uploads

## Quick Start
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy env file:
   ```bash
   cp .env.example .env
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```
6. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Environment Variables
Configuration is environment-driven from `ecommerce/settings.py`.

Core variables:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_TIME_ZONE`

Database variables:
- `DB_ENGINE` (`sqlite` or `mysql`)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (for MySQL)

## URL Routes
- Public:
  - `/` - home
  - `/productlist/` - product listing (paginated)
  - `/productdetails/<id>/` - product detail
- Auth/profile:
  - `/register/`, `/login/`, `/logout/`, `/profile/`, `/updateprofile/`
- Cart/orders:
  - `/cart/`, `/addtocart/<id>/`, `/post-order/<product_id>/<cart_id>/`, `/myorder/`
- Admin pages:
  - `/admin/dashboard/` - custom admin dashboard
  - `/products/` - product management
- Django admin:
  - `/django-admin/`

## Tests
Run tests with:
```bash
python manage.py test
```

## Improvements Added
- Environment-based settings with safer defaults
- Namespaced URL routing and template URL reversal (`{% url %}`)
- Safer object access with `get_object_or_404`
- Transaction-protected order creation and stock updates
- Improved eSewa callback handling and error paths
- Better admin dashboard metrics
- Baseline automated tests for auth/cart/admin and form validation
- Repository hygiene files: `.gitignore`, `requirements.txt`, `.env.example`
