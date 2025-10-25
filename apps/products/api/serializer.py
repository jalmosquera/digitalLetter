"""Product serializers for REST API operations.

This module provides serializers for the Product model, supporting multi-language
translations, ManyToMany relationships with categories and ingredients, and
CRUD operations through Django REST Framework.
"""

from typing import Any, Dict, List, Optional
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from apps.products.models import Product
from apps.categories.api.serializers import CategorySerializerGet
from apps.categories.models import Category
from apps.ingredients.api.serializers import IngredientSerializer
from apps.ingredients.models import Ingredient


class ProductSerializerPost(TranslatableModelSerializer):
    """Serializer for creating and updating Product instances with translations.

    Handles POST, PUT, and PATCH requests for product data, managing regular
    fields, translatable fields (name, description), and ManyToMany relationships
    (categories, ingredients). Provides custom create and update methods to
    properly handle all field types and relationships.

    Attributes:
        translations (TranslatedFieldsField): Exposes translatable fields
            (name, description) for the Product model.
        categories (PrimaryKeyRelatedField): Many-to-many relationship to Category
            model, accepts list of category IDs.
        ingredients (PrimaryKeyRelatedField): Many-to-many relationship to Ingredient
            model, accepts list of ingredient IDs (optional).

    Meta:
        model: Product model this serializer is based on.
        fields: All model fields are included in serialization.
        read_only_fields: Timestamp fields that cannot be modified via API.

    Example:
        >>> # Create product with translations and relationships
        >>> data = {
        ...     'translations': {
        ...         'en': {
        ...             'name': 'Margherita Pizza',
        ...             'description': 'Classic Italian pizza'
        ...         },
        ...         'es': {
        ...             'name': 'Pizza Margarita',
        ...             'description': 'Pizza italiana clásica'
        ...         }
        ...     },
        ...     'price': '12.99',
        ...     'stock': 50,
        ...     'available': True,
        ...     'categories': [1, 2],  # Category IDs
        ...     'ingredients': [3, 4, 5]  # Ingredient IDs
        ... }
        >>> serializer = ProductSerializerPost(data=data)
        >>> if serializer.is_valid():
        ...     product = serializer.save()
        >>>
        >>> # Update product (partial update)
        >>> data = {
        ...     'price': '13.99',
        ...     'stock': 45,
        ...     'ingredients': [3, 4, 5, 6]  # Add new ingredient
        ... }
        >>> serializer = ProductSerializerPost(
        ...     instance=product,
        ...     data=data,
        ...     partial=True
        ... )
        >>> if serializer.is_valid():
        ...     product = serializer.save()

    Note:
        - Handles translation data separately from regular fields
        - ManyToMany relationships set after instance creation
        - Categories are required, ingredients are optional
        - Supports partial updates for PATCH requests
        - Timestamps are auto-managed and cannot be set via API
    """

    translations = TranslatedFieldsField(shared_model=Product)
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all(),
        required=False
    )

    class Meta:
        """Meta options for ProductSerializerPost."""

        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data: Dict[str, Any]) -> Product:
        """Create a new Product instance with translations and relationships.

        Extracts translation data and ManyToMany relationships from validated_data,
        creates the base product instance with regular fields, sets the ManyToMany
        relationships, then iterates through each language to set translatable fields.

        Args:
            validated_data: Dictionary containing validated field data including:
                - 'translations': Dict with language codes and translatable fields
                - 'categories': List of Category instances
                - 'ingredients': List of Ingredient instances (optional)
                - Regular fields: price, stock, available, image

        Returns:
            Product: The newly created product instance with all translations
                and relationships saved.

        Example:
            >>> validated_data = {
            ...     'translations': {
            ...         'en': {'name': 'Caesar Salad', 'description': 'Fresh salad'},
            ...         'es': {'name': 'Ensalada César', 'description': 'Ensalada fresca'}
            ...     },
            ...     'price': Decimal('8.99'),
            ...     'stock': 30,
            ...     'available': True,
            ...     'categories': [<Category: Salads>],
            ...     'ingredients': [<Ingredient: Lettuce>, <Ingredient: Cheese>]
            ... }
            >>> product = serializer.create(validated_data)
            >>> product.categories.count()
            1
            >>> product.ingredients.count()
            2
        """
        translations = validated_data.pop('translations', {})
        categories = validated_data.pop('categories', [])
        ingredients = validated_data.pop('ingredients', [])
        instance = Product.objects.create(**validated_data)
        instance.categories.set(categories)
        instance.ingredients.set(ingredients)
        for lang_code, translation_fields in translations.items():
            instance.set_current_language(lang_code)
            for attr, value in translation_fields.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

    def update(self, instance: Product, validated_data: Dict[str, Any]) -> Product:
        """Update an existing Product instance with new data and translations.

        Updates regular fields, translatable fields, and ManyToMany relationships.
        Only updates categories and ingredients if they are present in validated_data,
        allowing for partial updates without affecting relationships.

        Args:
            instance: The existing product instance to update.
            validated_data: Dictionary containing validated field data including:
                - Optional 'translations': Dict with language codes and fields
                - Optional 'categories': List of Category instances
                - Optional 'ingredients': List of Ingredient instances
                - Optional regular fields: price, stock, available, image

        Returns:
            Product: The updated product instance with all changes saved.

        Example:
            >>> # Update price and stock only
            >>> validated_data = {
            ...     'price': Decimal('9.99'),
            ...     'stock': 25
            ... }
            >>> product = serializer.update(existing_product, validated_data)
            >>>
            >>> # Update translations and ingredients
            >>> validated_data = {
            ...     'translations': {
            ...         'en': {'name': 'Premium Caesar Salad'}
            ...     },
            ...     'ingredients': [<Ingredient: Romaine>, <Ingredient: Parmesan>]
            ... }
            >>> product = serializer.update(existing_product, validated_data)
        """
        translations = validated_data.pop('translations', {})
        categories = validated_data.pop('categories', None)
        ingredients = validated_data.pop('ingredients', None)
        if categories is not None:
            instance.categories.set(categories)
        if ingredients is not None:
            instance.ingredients.set(ingredients)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        for lang_code, translation_fields in translations.items():
            instance.set_current_language(lang_code)
            for attr, value in translation_fields.items():
                setattr(instance, attr, value)
        instance.save()
        return instance


class ProductSerializerGet(TranslatableModelSerializer):
    """Serializer for retrieving Product instances with nested relationships.

    Handles GET requests for product data, returning all fields including
    translatable fields (name, description) and nested serialized representations
    of related categories and ingredients. Customizes the price representation
    to include Euro currency symbol.

    Attributes:
        translations (TranslatedFieldsField): Exposes translatable fields
            (name, description) for the Product model.
        categories (CategorySerializerGet): Nested serializer for related categories,
            returns full category objects with translations (read-only).
        ingredients (IngredientSerializer): Nested serializer for related ingredients,
            returns full ingredient objects with translations (read-only).

    Meta:
        model: Product model this serializer is based on.
        fields: All model fields are included in serialization.
        read_only_fields: Timestamp fields that cannot be modified via API.

    Example:
        >>> # Retrieve product with nested relationships
        >>> serializer = ProductSerializerGet(product_instance)
        >>> serializer.data
        {
            'id': 1,
            'translations': {
                'en': {
                    'name': 'Margherita Pizza',
                    'description': 'Classic Italian pizza'
                },
                'es': {
                    'name': 'Pizza Margarita',
                    'description': 'Pizza italiana clásica'
                }
            },
            'price': '12.99 €',
            'stock': 50,
            'available': True,
            'image': '/media/Products/pizza.jpg',
            'categories': [
                {
                    'id': 1,
                    'translations': {
                        'en': {'name': 'Main Courses', 'description': '...'},
                        'es': {'name': 'Platos Principales', 'description': '...'}
                    },
                    'image': '/media/categories/main.jpg',
                    'created_at': '2024-01-15T10:30:00Z',
                    'updated_at': '2024-01-15T10:30:00Z'
                }
            ],
            'ingredients': [
                {
                    'id': 3,
                    'translations': {
                        'en': {'name': 'Mozzarella Cheese'},
                        'es': {'name': 'Queso Mozzarella'}
                    },
                    'icon': 'fa-cheese'
                }
            ],
            'created_at': '2024-01-15T11:00:00Z',
            'updated_at': '2024-01-15T11:00:00Z'
        }
        >>>
        >>> # Use in list view
        >>> products = Product.objects.all()
        >>> serializer = ProductSerializerGet(products, many=True)
        >>> serializer.data  # Returns list of serialized products

    Note:
        - Uses nested serializers for categories and ingredients
        - Price field is formatted with Euro symbol in representation
        - All relationships are read-only for GET operations
        - Automatically includes all translations for product and related objects
        - Timestamps are read-only and auto-managed
    """

    translations = TranslatedFieldsField(shared_model=Product)
    categories = CategorySerializerGet(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        """Meta options for ProductSerializerGet."""

        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def to_representation(self, instance: Product) -> Dict[str, Any]:
        """Convert Product instance to JSON-serializable dictionary with formatted price.

        Overrides the default representation to format the price field with
        Euro currency symbol for better display in frontend applications.

        Args:
            instance: The Product instance to serialize.

        Returns:
            Dict containing all serialized fields with price formatted as
                string with Euro symbol (e.g., "12.99 €").

        Example:
            >>> product = Product.objects.get(id=1)
            >>> product.price
            Decimal('12.99')
            >>> serializer = ProductSerializerGet(product)
            >>> serializer.data['price']
            '12.99 €'
        """
        data = super().to_representation(instance)
        data['price'] = f"{data['price']} €"
        return data
