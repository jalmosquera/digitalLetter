"""Ingredients API views module.

This module provides REST API viewsets for managing product ingredients with
internationalization support through django-parler. Ingredients can be created,
retrieved, updated, and deleted with multilingual name and description fields.

Typical usage example:
    GET /api/ingredients/ - List all ingredients with translations
    POST /api/ingredients/ - Create a new ingredient
    GET /api/ingredients/{id}/ - Retrieve a specific ingredient
    PUT /api/ingredients/{id}/ - Update an ingredient
    PATCH /api/ingredients/{id}/ - Partially update an ingredient
    DELETE /api/ingredients/{id}/ - Delete an ingredient
"""

from rest_framework import viewsets

from apps.ingredients.models import Ingredient
from apps.ingredients.api.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet for managing product ingredients with multilingual support.

    This viewset provides full CRUD operations for product ingredients with
    internationalization support via django-parler. Ingredients represent
    components or allergens that may be present in products, with translatable
    name and description fields for multiple languages.

    Attributes:
        queryset: QuerySet containing all Ingredient objects.
        serializer_class: IngredientSerializer for all operations.

    Endpoints:
        GET /api/ingredients/
            List all ingredients with their translations.
            Returns: List of ingredients with translated fields.
            Permissions: Default DRF permissions (typically authenticated).

        POST /api/ingredients/
            Create a new ingredient with translations.
            Request Body: IngredientSerializer schema with translations.
            Returns: Created ingredient with all translations.
            Permissions: Default DRF permissions (typically authenticated).

        GET /api/ingredients/{id}/
            Retrieve a specific ingredient by ID.
            Returns: Ingredient details with translations.
            Permissions: Default DRF permissions (typically authenticated).

        PUT /api/ingredients/{id}/
            Fully update an ingredient and its translations.
            Request Body: IngredientSerializer schema.
            Returns: Updated ingredient with translations.
            Permissions: Default DRF permissions (typically authenticated).

        PATCH /api/ingredients/{id}/
            Partially update an ingredient and its translations.
            Request Body: Partial IngredientSerializer schema.
            Returns: Updated ingredient with translations.
            Permissions: Default DRF permissions (typically authenticated).

        DELETE /api/ingredients/{id}/
            Delete an ingredient and all its translations.
            Returns: 204 No Content on success.
            Permissions: Default DRF permissions (typically authenticated).

    Examples:
        List all ingredients:
            GET /api/ingredients/
            Response: [
                {
                    "id": 1,
                    "name": "Milk",
                    "description": "Dairy product",
                    "translations": {
                        "en": {"name": "Milk", "description": "Dairy product"},
                        "es": {"name": "Leche", "description": "Producto lácteo"}
                    }
                }
            ]

        Create an ingredient:
            POST /api/ingredients/
            Body: {
                "translations": {
                    "en": {
                        "name": "Peanuts",
                        "description": "Common allergen"
                    },
                    "es": {
                        "name": "Cacahuetes",
                        "description": "Alérgeno común"
                    }
                }
            }

        Update an ingredient:
            PATCH /api/ingredients/1/
            Body: {
                "translations": {
                    "fr": {
                        "name": "Lait",
                        "description": "Produit laitier"
                    }
                }
            }

    Notes:
        - Supports full multilingual capabilities via django-parler.
        - Uses the same serializer for all CRUD operations.
        - Commonly used for allergen tracking and product composition.
        - Can be associated with multiple products through many-to-many
          relationships.
        - No custom permissions defined; uses Django REST Framework defaults.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
