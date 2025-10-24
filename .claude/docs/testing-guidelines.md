# Testing Guidelines

## 🎯 Filosofía

**"Tests de calidad sobre cantidad. Cobertura del 60-80% es profesional y suficiente."**

## Principios clave

- ✅ Tests útiles y mantenibles
- ✅ Cobertura objetivo: 60-80%
- ✅ Enfocado en lógica de negocio
- ❌ NO testear código de frameworks
- ❌ NO buscar 100% de cobertura
- ❌ NO tests innecesarios o triviales

## 📊 Cobertura de código

### Niveles de cobertura

| Cobertura | Calificación | Uso recomendado |
|-----------|--------------|-----------------|
| < 40% | ❌ Insuficiente | No recomendado |
| 40-60% | ⚠️ Básico | Aceptable para proyectos personales |
| **60-80%** | ✅ **Profesional** | **Recomendado** |
| 80-90% | 🌟 Excelente | Solo funcionalidad crítica |
| 90-100% | 🔥 Excesivo | Contraproducente |

## 📏 Límites por tipo de código

### Proporciones test/código

```
Modelo simple: 0.2x - 0.5x
  10 líneas de código = 2-5 líneas de test

Modelo con lógica: 0.5x - 1x
  50 líneas de código = 25-50 líneas de test

Endpoint CRUD: 1x - 1.5x
  50 líneas de código = 50-75 líneas de test
```

### Límites máximos por archivo

| Tipo de código | Máximo de líneas de test |
|----------------|--------------------------|
| Modelo simple | 20 líneas |
| Modelo con lógica | 50 líneas |
| Serializer simple | 30 líneas |
| Endpoint CRUD básico | 80 líneas |
| Endpoint con lógica | 150 líneas |

**NUNCA crear más de 200 líneas de test para un solo archivo.**

## ✅ Qué testear (Prioridad)

### 🔥 ALTA PRIORIDAD (siempre testear)

1. **Endpoints/APIs**
   - Status codes (200, 201, 400, 401, 403, 404)
   - Respuestas correctas
   - Validaciones
   - Permisos y autenticación

2. **Lógica de negocio custom**
   - Métodos con cálculos
   - Transformaciones de datos
   - Reglas de negocio
   - Algoritmos

3. **Validaciones críticas**
   - Validación de datos
   - Constraints de DB
   - Reglas de negocio

4. **Permisos y autenticación**
   - Usuario autenticado vs anónimo
   - Permisos por rol
   - Ownership de recursos

### ⚠️ MEDIA PRIORIDAD (testear si hay tiempo)

5. **Métodos de modelos** (solo si tienen lógica custom)
6. **Serializers con lógica**
7. **Casos edge**

### 🔽 BAJA PRIORIDAD (solo si sobra tiempo)

8. Métodos __str__
9. Configuración básica

## ❌ Qué NO testear

### NUNCA testear:

1. **Código de frameworks**
   - ❌ Django ORM básico
   - ❌ Django REST Framework sin modificar
   - ❌ Métodos de librerías externas
   - ❌ `manage.py` o comandos de Django
   - ❌ Migraciones

2. **Campos básicos de modelos**
   - ❌ `id`, `created_at`, `updated_at` auto-generados
   - ❌ Campos sin validaciones custom
   - ❌ Foreign Keys sin lógica

3. **Código trivial**
   - ❌ Getters/setters simples
   - ❌ Properties que solo retornan un campo
   - ❌ Métodos de una línea sin lógica
   - ❌ Imports
   - ❌ Configuraciones en settings.py

## 📝 Estructura de tests

### Template - Modelo simple

```python
from django.test import TestCase
from myapp.models import Category

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        """Test creating a category successfully"""
        category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.assertEqual(category.name, "Electronics")

    def test_category_str(self):
        """Test string representation"""
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")
```

### Template - Endpoint CRUD

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product_data = {
            'name': 'Laptop',
            'price': 999.99
        }

    def test_list_products(self):
        """Test listing products"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_authenticated(self):
        """Test creating product when authenticated"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/products/', self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unauthenticated(self):
        """Test creating product without authentication"""
        response = self.client.post('/api/products/', self.product_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

## 🎯 Regla 3-5

Para cada endpoint/función:
- **Mínimo 3 tests:** happy path + error común + validación
- **Máximo 5 tests:** agregar permisos + caso edge
- **NO MÁS de 5 tests** por función

## 🔍 Comandos útiles

```bash
# Todos los tests
python manage.py test

# Tests de una app
python manage.py test myapp

# Test específico
python manage.py test myapp.tests.test_models.ProductModelTest

# Con coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📋 Checklist de testing

- [ ] Tests cubren los endpoints principales
- [ ] Tests cubren la lógica de negocio custom
- [ ] Tests de permisos y autenticación
- [ ] Tests de validaciones críticas
- [ ] Cobertura entre 60-80%
- [ ] Ningún archivo de test tiene más de 200 líneas
- [ ] No hay tests de código de Django/frameworks
- [ ] Todos los tests pasan
- [ ] Tests tienen nombres descriptivos

## ⚠️ Errores comunes

### ❌ NO hacer:
```python
# Test innecesario - Django ya testea esto
def test_product_has_id(self):
    product = Product.objects.create(name="Laptop")
    self.assertIsNotNone(product.id)

# Test trivial - sin valor
def test_import_product_model(self):
    from myapp.models import Product
    self.assertIsNotNone(Product)
```

### ✅ SÍ hacer:
```python
# Test útil - verifica lógica de negocio
def test_product_discounted_price(self):
    product = Product.objects.create(name="Laptop", price=1000)
    discounted = product.get_discounted_price(0.10)
    self.assertEqual(discounted, 900)

# Test útil - verifica validación custom
def test_product_price_must_be_positive(self):
    with self.assertRaises(ValidationError):
        product = Product(name="Laptop", price=-100)
        product.full_clean()
```

## 💡 Tips finales

1. Escribe tests mientras desarrollas, no después
2. Un test = una cosa
3. Nombres descriptivos
4. AAA pattern: Arrange, Act, Assert
5. Coverage no es todo: 80% bien testeado > 100% mal testeado
