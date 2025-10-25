"""Product model module for digital menu management.

This module defines the Product model with multi-language support using
django-parler for translatable fields like name and description.
"""

from decimal import Decimal
from typing import Optional
from django.db import models
from django.core.validators import MinValueValidator
from parler.models import TranslatableModel, TranslatedFields
from apps.categories.models import Category
from apps.ingredients.models import Ingredient


class Product(TranslatableModel):
    """Product model for menu items with multi-language support.

    Represents a product in the digital menu system with translatable
    name and description fields. Supports price management, stock tracking,
    image uploads, and relationships with categories and ingredients.

    Attributes:
        translations (TranslatedFields): Translatable fields (name, description).
        price (Decimal): Product price with minimum value validation (> 0).
        stock (int): Available stock quantity, cannot be negative.
        available (bool): Whether the product is available for ordering.
        image (ImageField): Optional product image uploaded to 'Products/' directory.
        categories (ManyToManyField): Related categories for this product.
        ingredients (ManyToManyField): Ingredients used in this product.
        created_at (datetime): Timestamp when product was created.
        updated_at (datetime): Timestamp of last update.

    Translatable Fields:
        name (str): Product name in multiple languages (max 100 chars).
        description (str): Product description in multiple languages (optional).

    Example:
        >>> product = Product.objects.create(price=Decimal('12.99'), stock=50)
        >>> product.set_current_language('en')
        >>> product.name = "Margherita Pizza"
        >>> product.set_current_language('es')
        >>> product.name = "Pizza Margarita"
        >>> product.save()
        >>> product.categories.add(category1, category2)

    Note:
        - Price must be greater than 0.01
        - Stock cannot be negative
        - Uses django-parler for multi-language support
        - Table name preserved as 'products_products' for backward compatibility
    """

    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        description=models.TextField(blank=True, null=True),
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

    def __str__(self) -> str:
        """Return string representation of the product.

        Returns the product name in the current active language, or falls back
        to any available language translation. If no translation exists, returns
        a generic identifier with the primary key.

        Returns:
            str: Product name or "Product {pk}" if no translation available.

        Example:
            >>> product.set_current_language('en')
            >>> str(product)
            'Margherita Pizza'
        """
        return self.safe_translation_getter('name', any_language=True) or f"Product {self.pk}"

    class Meta:
        db_table = 'products_products'  # Keep old table name for backward compatibility
        verbose_name = "Product"
        verbose_name_plural = "Products"



