# Documentation Guidelines

## 🎯 Filosofía

**"Si necesitas más de 5 minutos para entender cómo correr el proyecto leyendo el README, la documentación está mal."**

## Principios clave

- ✅ Documentación concisa y útil
- ✅ Un solo README.md bien estructurado
- ✅ Enfocado en Quick Start
- ❌ NO documentación exhaustiva que nadie lee
- ❌ NO múltiples archivos separados (a menos que sea proyecto grande)

## 📄 Estructura del README.md

### Para proyectos pequeños/medianos (200-400 líneas)

```markdown
# Nombre del Proyecto

Brief description in one line.

[English](#english) | [Español](#español)

---

## English

### 📋 Overview
Brief description (2-3 lines explaining what the project does)

### 🚀 Quick Start
```bash
# Clone
git clone repo-url
cd project-name

# Install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver
```

### 📦 Tech Stack
- Django 4.2
- Django REST Framework
- PostgreSQL

### 🔑 Environment Variables
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 📡 API Endpoints

**Authentication**
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration

**Products**
- `GET /api/products/` - List products
- `POST /api/products/` - Create product

### 🧪 Testing

```bash
python manage.py test
coverage run --source='.' manage.py test
coverage report
```

### 🚀 Deployment

**Railway/Render:**
1. Create new project
2. Connect GitHub repo
3. Add environment variables
4. Deploy

### 📝 License
MIT

---

## Español
[Misma estructura en español]
```

## ✅ Qué incluir

### Esencial (siempre):
1. Descripción breve (1-2 líneas)
2. Quick Start (comandos para clonar, instalar y correr)
3. Tech Stack (lista de tecnologías)
4. Environment Variables (qué variables necesita el .env)
5. Endpoints principales (lista simple)
6. Database Schema (entidades principales)
7. Comandos útiles (test, migrate, deploy)

## ❌ Qué NO incluir

- ❌ Documentación detallada de cada función/clase
- ❌ Explicación de cómo funciona Django/el framework
- ❌ Schema completo de DB con todos los tipos de datos
- ❌ Historia del proyecto
- ❌ Múltiples archivos separados para cosas que caben en el README
- ❌ Tutoriales de Git
- ❌ Troubleshooting extenso

## 🌍 Documentación bilingüe

### Estructura recomendada:

**Opción 1: Todo en un archivo (recomendado)**
```markdown
# Project Name

[English](#english) | [Español](#español)

## English
[Contenido en inglés]

## Español
[Contenido en español]
```

## 🎨 Formato y estilo

### Usar emojis para secciones (opcional pero recomendado)

```markdown
📋 Overview
🚀 Quick Start
📦 Tech Stack
🔑 Environment Variables
📡 API Endpoints
🗄️ Database Schema
🧪 Testing
🚀 Deployment
📝 License
```

### Code blocks
- Siempre especificar el lenguaje: ```bash, ```python
- Incluir comentarios si es necesario
- Mantener ejemplos cortos

## 📋 Checklist de documentación

- [ ] Alguien nuevo puede clonar y correr el proyecto en menos de 5 minutos
- [ ] Todas las environment variables están documentadas
- [ ] Los comandos están probados y funcionan
- [ ] Las tecnologías principales están listadas
- [ ] El propósito del proyecto es claro en 2-3 líneas
- [ ] No hay más de 400 líneas (si es proyecto pequeño/mediano)
- [ ] No hay información redundante
- [ ] Los links funcionan
- [ ] Si es bilingüe, ambas versiones dicen lo mismo

## ⚠️ Errores comunes

- ❌ Documentar TODO en el README
- ❌ Comandos que no funcionan
- ❌ Falta de ejemplos de .env
- ❌ No especificar versiones de tecnologías
- ❌ Documentación desactualizada
- ❌ Múltiples archivos innecesarios
