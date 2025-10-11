from django.core.management.base import BaseCommand
from django.db import transaction

from apps.categories.models import Category
from apps.ingredients.models import Ingredients
from apps.products.models import Products


class Command(BaseCommand):
    help = "Populate demo data: categories -> ingredients -> products (ES/EN)."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding demo data..."))

        categories = self._seed_categories()
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(categories)} categories"))

        ingredients = self._seed_ingredients()
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(ingredients)} ingredients"))

        products = self._seed_products(categories, ingredients)
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(products)} products"))

        self.stdout.write(self.style.SUCCESS("Seeding completed."))

    def _seed_categories(self):
        created = []
        data = [
            {"es": {"name": "Entradas", "description": "Productos para iniciar"},
             "en": {"name": "Starters", "description": "Begin your meal"}},
            {"es": {"name": "Productos principales", "description": "Productos principales"},
             "en": {"name": "Mains", "description": "Main dishes"}},
            {"es": {"name": "Postres", "description": "Dulces finales"},
             "en": {"name": "Desserts", "description": "Sweet endings"}},
        ]
        for item in data:
            obj = Category.objects.create()
            obj.set_current_language('es')
            obj.name = item["es"]["name"]
            obj.description = item["es"].get("description")
            obj.save()
            obj.set_current_language('en')
            obj.name = item["en"]["name"]
            obj.description = item["en"].get("description")
            obj.save()
            created.append(obj)
        return created

    def _seed_ingredients(self):
        created = []
        data = [
            {"es": {"name": "Tomate"}, "en": {"name": "Tomato"}},
            {"es": {"name": "Queso"}, "en": {"name": "Cheese"}},
            {"es": {"name": "Albahaca"}, "en": {"name": "Basil"}},
        ]
        for item in data:
            obj = Ingredients.objects.create()
            obj.set_current_language('es')
            obj.name = item["es"]["name"]
            obj.save()
            obj.set_current_language('en')
            obj.name = item["en"]["name"]
            obj.save()
            created.append(obj)
        return created

    def _seed_products(self, categories, ingredients):
        created = []
        # simple mapping helpers
        cat_by_name = {c.safe_translation_getter('name', any_language=True): c for c in categories}
        ing_by_name = {i.safe_translation_getter('name', any_language=True): i for i in ingredients}

        data = [
            {
                "translations": {
                    "es": {"name": "Bruschetta", "description": "Pan con tomate y albahaca"},
                    "en": {"name": "Bruschetta", "description": "Bread with tomato and basil"},
                },
                "price": 6.50,
                "stock": 100,
                "available": True,
                "categories": ["Entradas"],
                "ingredients": ["Tomate", "Albahaca"],
            },
            {
                "translations": {
                    "es": {"name": "Pizza Margarita", "description": "Queso y albahaca"},
                    "en": {"name": "Margherita Pizza", "description": "Cheese and basil"},
                },
                "price": 12.00,
                "stock": 50,
                "available": True,
                "categories": ["Productos principales"],
                "ingredients": ["Tomate", "Queso", "Albahaca"],
            },
            {
                "translations": {
                    "es": {"name": "Tiramisú", "description": "Clásico italiano"},
                    "en": {"name": "Tiramisu", "description": "Italian classic"},
                },
                "price": 7.50,
                "stock": 40,
                "available": True,
                "categories": ["Postres"],
                "ingredients": [],
            },
        ]

        for item in data:
            p = Products.objects.create(price=item["price"], stock=item["stock"], available=item["available"]) 
            p.set_current_language('es')
            p.name = item["translations"]["es"]["name"]
            p.description = item["translations"]["es"].get("description")
            p.save()
            p.set_current_language('en')
            p.name = item["translations"]["en"]["name"]
            p.description = item["translations"]["en"].get("description")
            p.save()

            for cat_name in item["categories"]:
                c = cat_by_name.get(cat_name)
                if c:
                    p.categories.add(c)
            for ing_name in item["ingredients"]:
                ing = ing_by_name.get(ing_name)
                if ing:
                    p.ingredients.add(ing)
            created.append(p)
        return created





