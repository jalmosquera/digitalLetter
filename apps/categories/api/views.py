"""Categories API views module.

This module provides REST API viewsets for managing product categories with
internationalization support through django-parler. Categories can be created,
retrieved, updated, and deleted with multilingual name and description fields.

Typical usage example:
    GET /api/categories/ - List all categories with translations
    POST /api/categories/ - Create a new category
    GET /api/categories/{id}/ - Retrieve a specific category
    PUT /api/categories/{id}/ - Update a category
    PATCH /api/categories/{id}/ - Partially update a category
    DELETE /api/categories/{id}/ - Delete a category
"""

from typing import Any

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.categories.models import Category
from apps.categories.api.serializers import (
    CategorySerializerGet,
    CategorySerializerPost,
)


class CategoriesView(viewsets.ModelViewSet):
    """ViewSet for managing product categories with multilingual support.

    This viewset provides CRUD operations for product categories with full
    internationalization support via django-parler. It uses different serializers
    for read and write operations to optimize data presentation and validation.

    Attributes:
        queryset: QuerySet containing all Category objects.
        permission_classes: List containing AllowAny permission (public access).

    Endpoints:
        GET /api/categories/
            List all categories with their translations.
            Returns: List of categories with translated fields.
            Permissions: AllowAny (public access).

        POST /api/categories/
            Create a new category with translations.
            Request Body: CategorySerializerPost schema.
            Returns: Created category with all translations.
            Permissions: AllowAny (public access).

        GET /api/categories/{id}/
            Retrieve a specific category by ID.
            Returns: Category details with translations.
            Permissions: AllowAny (public access).

        PUT /api/categories/{id}/
            Fully update a category and its translations.
            Request Body: CategorySerializerPost schema.
            Returns: Updated category with translations.
            Permissions: AllowAny (public access).

        PATCH /api/categories/{id}/
            Partially update a category and its translations.
            Request Body: Partial CategorySerializerPost schema.
            Returns: Updated category with translations.
            Permissions: AllowAny (public access).

        DELETE /api/categories/{id}/
            Delete a category and all its translations.
            Returns: 204 No Content on success.
            Permissions: AllowAny (public access).

    Examples:
        List all categories:
            GET /api/categories/
            Response: [
                {
                    "id": 1,
                    "name": "Beverages",
                    "description": "Hot and cold drinks",
                    "translations": {...}
                }
            ]

        Create a category:
            POST /api/categories/
            Body: {
                "translations": {
                    "en": {"name": "Desserts", "description": "Sweet treats"},
                    "es": {"name": "Postres", "description": "Dulces"}
                }
            }

    Notes:
        - Uses CategorySerializerGet for read operations (list, retrieve).
        - Uses CategorySerializerPost for write operations (create, update).
        - Responses for create/update/partial_update use CategorySerializerGet
          to include all translations in the response.
        - All endpoints are publicly accessible (AllowAny permission).
        - Supports django-parler for multilingual fields.
    """

    queryset = Category.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self) -> type[Serializer]:
        """Return the appropriate serializer class based on the action.

        Returns:
            CategorySerializerGet for list and retrieve actions.
            CategorySerializerPost for create, update, and delete actions.
        """
        if self.action in ['list', 'retrieve']:
            return CategorySerializerGet
        return CategorySerializerPost

    def get_serializer(self, *args: Any, **kwargs: Any) -> Serializer:
        """Get serializer instance with custom logic for write operations.

        For create/update/partial_update actions, returns CategorySerializerGet
        instance to ensure the response includes all translations.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Serializer instance appropriate for the current action.

        Notes:
            This ensures that write operations return the full category object
            with all translations, improving client-side data consistency.
        """
        # For create/update/partial_update responses, use GET serializer
        # to include all translations in the response
        if self.action in ['create', 'update', 'partial_update']:
            kwargs.setdefault('context', self.get_serializer_context())
            return CategorySerializerGet(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)
