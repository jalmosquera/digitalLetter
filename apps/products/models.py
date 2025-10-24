from django.db import models
from django.core.validators import MinValueValidator
from parler.models import TranslatableModel, TranslatedFields
from apps.categories.models import Category
from apps.ingredients.models import Ingredient

class Product(TranslatableModel):
    '''Model definition for Product.'''
    translations = TranslatedFields(
        name = models.CharField(max_length=100),
        description = models.TextField(blank=True, null=True),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='Products/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Product {self.pk}"

    class Meta:
        db_table = 'products_products'  # Keep old table name
        verbose_name = "Product"
        verbose_name_plural = "Products"



