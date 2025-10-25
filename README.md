# DigitalLetter API

RESTful API for digital menu management built with Django and Django REST Framework, featuring multi-language support and role-based access control.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16+-red.svg)](https://www.django-rest-framework.org/)
[![codecov](https://codecov.io/gh/Jal7823/digitalLetter/branch/main/graph/badge.svg)](https://codecov.io/gh/Jal7823/digitalLetter)

> 📖 [Versión en Español](README_ES.md)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

DigitalLetter API is a comprehensive backend solution for managing digital restaurant menus. It provides multi-language support for products and categories, role-based user management, and a complete RESTful API for integration with frontend applications.

The system supports:
- Multi-language content (English/Spanish) for products and categories
- Three user roles: client, employee, and boss
- Complete CRUD operations for products, categories, ingredients, and company information
- JWT-based authentication
- Automatic API documentation with Swagger/ReDoc

## ✨ Features

- **Multi-language Support**: Products and categories with translations using django-parler
- **Role-Based Access Control**: Three distinct user roles (client, employee, boss)
- **RESTful API**: Complete CRUD operations for all resources
- **JWT Authentication**: Secure token-based authentication
- **API Documentation**: Auto-generated Swagger UI and ReDoc documentation
- **Image Management**: Support for product and company images
- **Ingredient Tracking**: Manage and track product ingredients
- **Filtering & Search**: Advanced filtering capabilities with django-filter

## 🛠️ Tech Stack

**Backend:**
- Python 3.12+
- Django 5.2.3
- Django REST Framework 3.16
- SQLite (development) / PostgreSQL (production ready)

**Key Libraries:**
- django-parler 2.3 - Multi-language support
- drf-spectacular 0.28 - API documentation
- djangorestframework-simplejwt 5.5 - JWT authentication
- django-filter 24.3 - Advanced filtering
- Pillow 11.2 - Image processing

**Development & Testing:**
- pytest 8.4 - Testing framework
- pytest-django 4.11 - Django testing utilities
- coverage 7.9 - Code coverage

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/jalmosquera/digitalLetter.git
cd digitalLetter
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
# Follow the prompts:
# - Username
# - Email
# - Name
# - Password
```

7. **Run development server:**
```bash
python manage.py runserver
```

Visit http://localhost:8000 to see the Swagger UI documentation.

## 📚 API Documentation

Interactive API documentation is available at:

- **Swagger UI:** http://localhost:8000/ (root)
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

### Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. **Obtain token:**
```bash
POST /api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

2. **Use token in requests:**
```bash
GET /api/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

3. **Refresh token:**
```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Main Endpoints

| Resource | Endpoint | Methods | Description |
|----------|----------|---------|-------------|
| Products | `/api/products/` | GET, POST, PUT, DELETE | Manage products with translations |
| Categories | `/api/categories/` | GET, POST, PUT, DELETE | Manage categories with translations |
| Ingredients | `/api/ingredients/` | GET, POST, PUT, DELETE | Manage ingredients with translations |
| Users | `/api/users/` | GET, POST, PUT, DELETE | User management with roles |
| Company | `/api/company/` | GET, POST, PUT, DELETE | Company information |
| Auth | `/api/token/` | POST | Obtain JWT tokens |
| Auth | `/api/token/refresh/` | POST | Refresh JWT tokens |

### Example: Create a Product

```bash
POST /api/products/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "translations": {
    "en": {
      "name": "Margherita Pizza",
      "description": "Classic Italian pizza with tomato and mozzarella"
    },
    "es": {
      "name": "Pizza Margarita",
      "description": "Pizza italiana clásica con tomate y mozzarella"
    }
  },
  "price": "12.99",
  "stock": 50,
  "available": true,
  "categories": [1, 2],
  "ingredients": [1, 3, 5]
}
```

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development - SQLite)
# SQLite is used by default, no configuration needed

# Database (Production - PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost:5432/digitalletter

# CORS (if using frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Language
LANGUAGE_CODE=es
```

See `.env.example` for a complete list of configuration options.

## 📁 Project Structure

```
digitalLetter/
├── apps/
│   ├── categories/      # Category management (with translations)
│   │   ├── api/         # API views, serializers, routers
│   │   ├── models.py
│   │   └── admin.py
│   ├── products/        # Product management (with translations)
│   │   ├── api/
│   │   ├── models.py
│   │   └── admin.py
│   ├── ingredients/     # Ingredient management (with translations)
│   │   ├── api/
│   │   ├── models.py
│   │   └── admin.py
│   ├── users/           # User management with roles
│   │   ├── api/
│   │   ├── models.py
│   │   └── admin.py
│   └── company/         # Company information
│       ├── api/
│       ├── models.py
│       └── admin.py
├── core/                # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/               # User uploaded files
├── static/              # Static files
├── manage.py
├── requirements.txt
└── README.md
```

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
coverage run --source='.' -m pytest
coverage report
coverage html  # Generate HTML report
```

## 🚀 Deployment

### Deploy to Railway

1. **Push your code to GitHub**

2. **Go to [Railway](https://railway.app) and create new project**

3. **Select "Deploy from GitHub"**

4. **Choose your repository**

5. **Add PostgreSQL database:**
   - New → Database → PostgreSQL

6. **Set environment variables in Railway dashboard:**
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-app.railway.app
   - `DATABASE_URL`: (automatically set by Railway PostgreSQL)

7. **Add start command in Railway settings:**
```bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn core.wsgi
```

8. **Deploy!**

### Production Considerations

- Set `DEBUG=False` in production
- Use PostgreSQL instead of SQLite
- Configure proper `ALLOWED_HOSTS`
- Serve static files with WhiteNoise or CDN
- Use environment variables for sensitive data
- Enable HTTPS only cookies
- Configure CORS properly

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Commit Convention

This project follows conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Jalberth Mosquera**
- GitHub: [@jalmosquera](https://github.com/jalmosquera)

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

**Note:** This is the main documentation in English. For Spanish version, see [README_ES.md](README_ES.md).
