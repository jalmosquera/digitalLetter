import json
from django.db import transaction
from apps.products.models import Products
from apps.ingredients.models import Ingredients
from apps.categories.models import Category

# Ruta de la imagen común para todos los productos (relativa a MEDIA_ROOT)
PRODUCT_IMAGE_SRC = "Products/2.jpeg"

# Carga el JSON
with open('menu_text.JSON', encoding='utf-8') as f:
    carta = json.load(f)


# Helper para obtener o crear ingredientes en varias traducciones y con icono
def get_or_create_ingredient(ingredient_dict):
    name_es = ingredient_dict["name_es"].strip()
    name_en = ingredient_dict.get("name_en", name_es).strip()
    icon = ingredient_dict.get("icon", "")
    
    # Buscar ingrediente existente por nombre en español
    ingredient = Ingredients.objects.filter(
        translations__name=name_es
    ).first()
    
    if not ingredient:
        ingredient = Ingredients.objects.create(icon=icon)
    
    ingredient.set_current_language('es')
    ingredient.name = name_es
    ingredient.save()
    ingredient.set_current_language('en')
    ingredient.name = name_en
    ingredient.save()
    return ingredient

# Helper para obtener o crear categoría traducida
def get_or_create_category(cat_es, cat_en):
    # Buscar categoría existente por nombre en español
    cat = Category.objects.filter(
        translations__name=cat_es.strip()
    ).first()
    
    if not cat:
        cat = Category.objects.create()
    
    cat.set_current_language('es')
    cat.name = cat_es.strip()
    cat.save()
    cat.set_current_language('en')
    cat.name = cat_en.strip()
    cat.save()
    return cat


# Función para procesar un producto individual
def process_product(product_dict, category):
    name_es = product_dict["name_es"].strip()
    name_en = product_dict.get("name_en", name_es).strip()
    desc_es = product_dict.get("description_es", "")
    desc_en = product_dict.get("description_en", desc_es)
    price = float(product_dict.get("price", 0.0))

    # Crear producto
    product = Products.objects.create(
        price=price,
        stock=10,
        available=True,
        image=PRODUCT_IMAGE_SRC
    )
    # Traducción español
    product.set_current_language('es')
    product.name = name_es
    product.description = desc_es
    product.save()
    # Traducción inglés
    product.set_current_language('en')
    product.name = name_en
    product.description = desc_en
    product.save()
    # Categoría
    product.categories.add(category)
    # Ingredientes
    for ing_dict in product_dict.get("ingredients", []):
        ingredient = get_or_create_ingredient(ing_dict)
        product.ingredients.add(ingredient)
    product.save()


# Usar transacción para asegurar consistencia
with transaction.atomic():
    for block in carta:
        # Verificar si es una categoría con productos o un producto individual
        if "products" in block:
            # Es una categoría con productos
            cat_es = block.get("category_es", "Sin categoría")
            cat_en = block.get("category_en", cat_es)
            category = get_or_create_category(cat_es, cat_en)
            
            for product_dict in block["products"]:
                process_product(product_dict, category)
        else:
            # Es un producto individual sin categoría específica
            category = get_or_create_category("Sin categoría", "No category")
            process_product(block, category)

print("¡Carta insertada correctamente en la base de datos en español e inglés con emojis y categorías!")
