"""Product serializers for REST API operations.

This module provides serializers for the Product model, supporting multi-language
translations, ManyToMany relationships with categories and ingredients, and
CRUD operations through Django REST Framework.
"""

import json
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

    This serializer supports TWO input formats:

    1. JSON format (nested) - Use when NOT sending files:
       - Content-Type: application/json
       - Translations as nested objects
       - Categories/ingredients as arrays

    2. form-data format (flat) - Use when sending image files:
       - Content-Type: multipart/form-data
       - Translations as flat fields (name_en, name_es, etc.)
       - Categories/ingredients as comma-separated strings or JSON strings

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

    Example (JSON format):
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

    Example (form-data format with image):
        >>> # Frontend: Use FormData when sending image
        >>> # const formData = new FormData();
        >>> # formData.append('name_en', 'Margherita Pizza');
        >>> # formData.append('name_es', 'Pizza Margarita');
        >>> # formData.append('description_en', 'Classic Italian pizza');
        >>> # formData.append('description_es', 'Pizza italiana clásica');
        >>> # formData.append('categories', '1,2');  // or JSON: '[1,2]'
        >>> # formData.append('ingredients', '3,4,5');  // or JSON: '[3,4,5]'
        >>> # formData.append('price', '12.99');
        >>> # formData.append('stock', '50');
        >>> # formData.append('image', imageFile);

    Note:
        - Handles translation data separately from regular fields
        - ManyToMany relationships set after instance creation
        - Categories are required, ingredients are optional
        - Supports partial updates for PATCH requests
        - Timestamps are auto-managed and cannot be set via API
        - Automatically detects and transforms flat form-data to nested structure
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

    def to_internal_value(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform flat form-data fields to nested format expected by serializer.

        This method allows the serializer to accept two input formats:

        1. JSON format (nested structure):
           {
               "translations": {
                   "en": {"name": "...", "description": "..."},
                   "es": {"name": "...", "description": "..."}
               },
               "categories": [1, 2],
               "ingredients": [3, 4]
           }

        2. form-data format (flat fields):
           {
               "name_en": "...",
               "name_es": "...",
               "description_en": "...",
               "description_es": "...",
               "categories": "1,2" or "[1,2]",
               "ingredients": "3,4,5" or "[3,4,5]"
           }

        Args:
            data: Raw input data from request, can be nested JSON or flat form-data.

        Returns:
            Dictionary with normalized nested structure expected by parent serializer.

        Raises:
            serializers.ValidationError: If categories/ingredients format is invalid.
        """
        # Convert QueryDict to regular dict to avoid list wrapping issues
        if hasattr(data, 'lists'):
            # It's a QueryDict, convert to dict extracting first value from lists
            new_data = {}
            for key, value_list in data.lists():
                if len(value_list) == 1:
                    new_data[key] = value_list[0]
                else:
                    new_data[key] = value_list
            data = new_data
        else:
            # Regular dict, just copy
            data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Helper function to extract value from lists (if still needed)
        def get_value(value):
            """Extract actual value from list format."""
            if isinstance(value, list) and len(value) > 0:
                return value[0]
            return value

        # Handle flat translation fields (name_en, name_es, etc.)
        # Check if flat fields exist instead of nested translations
        supported_languages = ['en', 'es']
        translation_fields = ['name', 'description']

        has_flat_translations = any(
            f"{field}_{lang}" in data
            for field in translation_fields
            for lang in supported_languages
        )

        if has_flat_translations and 'translations' not in data:
            # Convert flat fields to nested structure
            translations = {}
            for lang in supported_languages:
                lang_data = {}
                for field in translation_fields:
                    field_key = f"{field}_{lang}"
                    if field_key in data:
                        # Extract value and handle QueryDict list format
                        value = get_value(data.pop(field_key))
                        lang_data[field] = value

                if lang_data:  # Only add if we have data for this language
                    translations[lang] = lang_data

            if translations:
                data['translations'] = translations

        # Handle categories field - convert string or JSON string to list
        if 'categories' in data:
            categories_value = get_value(data['categories'])
            if isinstance(categories_value, str):
                try:
                    # Try parsing as JSON array first
                    categories = json.loads(categories_value)
                    if not isinstance(categories, list):
                        categories = [categories]
                except (json.JSONDecodeError, ValueError):
                    # If not JSON, try comma-separated values
                    categories = [int(cat.strip()) for cat in categories_value.split(',') if cat.strip()]
                data['categories'] = categories
            elif not isinstance(categories_value, list):
                # Single value, convert to list
                data['categories'] = [categories_value]

        # Handle ingredients field - convert string or JSON string to list
        if 'ingredients' in data:
            ingredients_value = get_value(data['ingredients'])
            if isinstance(ingredients_value, str):
                try:
                    # Try parsing as JSON array first
                    ingredients = json.loads(ingredients_value)
                    if not isinstance(ingredients, list):
                        ingredients = [ingredients]
                except (json.JSONDecodeError, ValueError):
                    # If not JSON, try comma-separated values
                    ingredients = [int(ing.strip()) for ing in ingredients_value.split(',') if ing.strip()]
                data['ingredients'] = ingredients
            elif not isinstance(ingredients_value, list):
                # Single value, convert to list
                data['ingredients'] = [ingredients_value]

        return super().to_internal_value(data)

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
