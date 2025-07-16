
# DigitalLetter API

Welcome to **DigitalLetter API** — a RESTful backend built with Django and Django REST Framework to manage categories, products (dishes), and users with differentiated roles.

## 🚀 Tech Stack

- Python 3.11
- Django 5.2
- Django REST Framework
- Simple JWT for authentication
- DRF Spectacular for OpenAPI/Swagger docs
- Pytest for testing
- Docker & Docker Compose
- SQLite as default database
- `django-parler` for multilingual support (categories and products only)

---

## 📁 Documentation

Extended documentation available:

- Project architecture
- API routes and behaviors
- Translation support

## 📦 Project Structure

```
apps/
├── categories/    # Category management (with translations)
├── products/      # Dishes/products, related to categories (ManyToMany, with translations)
├── users/         # Advanced user management (client, employe, boss roles)
├── company/       # General company info (no translations)
core/
├── settings/      # Environment-based settings
├── urls.py
├── wsgi.py
```

## 🔍 Main Endpoints

| Resource        | URL Base           | Methods           | Description                                |
|----------------|--------------------|-------------------|--------------------------------------------|
| Categories      | /api/categories/   | GET, POST, PUT…   | CRUD for product categories                |
| Products (Plates) | /api/products/     | GET, POST, PUT…   | CRUD for products related to categories    |
| Employees       | /api/employe/      | GET, POST, PATCH  | User management for `employe` role         |
| Clients         | /api/clients/      | GET, POST, PATCH  | User management for `client` role          |
| Auth (JWT)      | /api/token/        | POST              | Login with JWT (SimpleJWT)                 |
| Current User    | /api/me/           | GET, PATCH        | Authenticated user's profile               |
| Change Password | /api/change-password/ | POST           | Change password securely                   |

## 📚 API Documentation

Auto-generated with DRF Spectacular:

- Swagger UI: `/`
- Redoc: `/api/redoc/`
- OpenAPI JSON schema: `/api/schema/`

## 🔐 Authentication & Permissions

- JWT via SimpleJWT (`/api/token/` and `/api/token/refresh/`)
- Custom permissions:
  - `IsStaff`
  - `IsEmploye`
  - `IsBoss`
  - `IsStaffOrEmploye`
- Some endpoints open (`AllowAny`) in development mode

## 🧑 Key Models

### Users
- Extends `AbstractUser`
- Custom fields: `role`, `address`, `location`, `province`, `phone`, `image`
- Roles: `client`, `employe`, `boss`
- Secure password handling with `set_password`

### Plates (Products)
- Fields: `name`, `description`, `price`, `stock`, `available`, `image`
- ManyToMany relation with `Category`
- Translations for `name` and `description` via `django-parler`
- Separated serializers:
  - `ProductSerializerGet` (read)
  - `ProductSerializerPost` (write)
- Price validation to prevent negative values

## ⚙️ Environment Configuration

Environment variables via `.env` file. Example:

```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_ENV=development
DEBUG=True
```

Loaded automatically with `python-dotenv` in `manage.py`.

### Database
- Default: SQLite (for development)
- To switch to PostgreSQL: edit `core/settings/production.py`

## 🐳 Docker Ready

Run with Docker:

```bash
docker-compose up --build
```

Ensure `.env` exists and ports/volumes are properly configured in `docker-compose.yml`.

## ✅ Testing

Using `pytest` and `pytest-django`:

```bash
pytest
```

- Use `@pytest.mark.django_db` for DB access in tests
- Tests include categories, products, users, permissions
- Avoid image tests unless required

## 🔀 API Routing

Registered using `DefaultRouter`:

```python
router.register(r'categories', CategoriesView, basename='categories')
router.register(r'products', ProductsViewSetGet, basename='products')
router.register(r'employe', RegisterEmploye, basename='employe')
router.register(r'clients', RegisterClients, basename='clients')
```

## 🧠 Best Practices

- Separate serializers for read/write logic
- Custom field validations in `serializers.py`
- Viewsets + routers = clean RESTful API
- Role-based permission classes
- Environment-based settings using `DJANGO_ENV`
- Translation support via `django-parler`

## 📬 Contact

Want to contribute or have questions?  
Feel free to reach out — happy to help!

---

🎉 Thanks for using **DigitalLetter API**!
