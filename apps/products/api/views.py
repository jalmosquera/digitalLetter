"""Products API views module.

This module provides REST API viewsets for managing products in the digital
menu system. Products support internationalization, filtering, searching, and
ordering capabilities. They can be associated with categories and ingredients.

Typical usage example:
    GET /api/products/ - List all available products
    GET /api/products/?categories=1&ordering=price - Filter and sort products
    GET /api/products/?search=pizza - Search products by name or description
    POST /api/products/ - Create a new product (authenticated users only)
    GET /api/products/{id}/ - Retrieve a specific product
    PUT /api/products/{id}/ - Update a product (authenticated users only)
    PATCH /api/products/{id}/ - Partially update a product (authenticated)
    DELETE /api/products/{id}/ - Delete a product (authenticated users only)
"""

from typing import Any

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import Serializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.products.models import Product
from apps.products.api.serializer import ProductSerializerPost, ProductSerializerGet


@extend_schema_view(
    list=extend_schema(
        tags=['products'],
        responses=ProductSerializerGet(many=True),
    ),
    create=extend_schema(
        tags=['products'],
        request=ProductSerializerPost,
        responses={
            201: ProductSerializerGet,
            400: OpenApiResponse(description='Invalid data'),
        },
    ),
    retrieve=extend_schema(
        tags=['products'],
        responses={
            200: ProductSerializerGet,
            404: OpenApiResponse(description='Not found'),
        },
    ),
    update=extend_schema(
        tags=['products'],
        request=ProductSerializerPost,
        responses={
            200: ProductSerializerGet,
            400: OpenApiResponse(description='Invalid data'),
        },
    ),
    partial_update=extend_schema(
        tags=['products'],
        request=ProductSerializerPost,
        responses={
            200: ProductSerializerGet,
            400: OpenApiResponse(description='Invalid data'),
        },
    ),
    destroy=extend_schema(
        tags=['products'],
        responses={204: OpenApiResponse(description='Deleted')},
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for managing products with advanced filtering and search.

    This viewset provides comprehensive product management with multilingual
    support, filtering, searching, and ordering capabilities. Products can be
    filtered by availability, categories, and ingredients, and searched by
    translated name and description fields.

    Attributes:
        queryset: QuerySet filtered to show only available products.
        permission_classes: IsAuthenticatedOrReadOnly - read-only for anonymous
            users, full access for authenticated users.
        filter_backends: List of filter backends (DjangoFilter, Search, Ordering).
        filterset_fields: Fields available for filtering (available, categories,
            ingredients).
        ordering_fields: Fields available for ordering (price, stock, created_at,
            updated_at).
        search_fields: Fields searchable via query parameter (translated name
            and description).

    Endpoints:
        GET /api/products/
            List all available products with translations.
            Query Parameters:
                - available: Filter by availability (true/false)
                - categories: Filter by category ID(s)
                - ingredients: Filter by ingredient ID(s)
                - ordering: Sort by field (price, -price, stock, created_at)
                - search: Search in name and description
            Returns: List of products with full details.
            Permissions: AllowAny (public access).

        POST /api/products/
            Create a new product with translations.
            Request Body: ProductSerializerPost schema.
            Returns: Created product with all details (201 Created).
            Permissions: IsAuthenticated (authenticated users only).

        GET /api/products/{id}/
            Retrieve a specific product by ID.
            Returns: Product details with translations and relationships.
            Permissions: AllowAny (public access).

        PUT /api/products/{id}/
            Fully update a product and its translations.
            Request Body: ProductSerializerPost schema.
            Returns: Updated product with all details.
            Permissions: IsAuthenticated (authenticated users only).

        PATCH /api/products/{id}/
            Partially update a product and its translations.
            Request Body: Partial ProductSerializerPost schema.
            Returns: Updated product with all details.
            Permissions: IsAuthenticated (authenticated users only).

        DELETE /api/products/{id}/
            Delete a product (soft delete recommended).
            Returns: 204 No Content on success.
            Permissions: IsAuthenticated (authenticated users only).

    Examples:
        List all products:
            GET /api/products/
            Response: [
                {
                    "id": 1,
                    "name": "Margherita Pizza",
                    "description": "Classic Italian pizza",
                    "price": "12.99",
                    "stock": 50,
                    "available": true,
                    "categories": [1, 2],
                    "ingredients": [3, 4, 5]
                }
            ]

        Filter products by category:
            GET /api/products/?categories=1
            Returns products in category 1.

        Search products:
            GET /api/products/?search=pizza
            Returns products with "pizza" in name or description.

        Order products by price:
            GET /api/products/?ordering=price
            Returns products sorted by price ascending.
            Use ?ordering=-price for descending.

        Create a product:
            POST /api/products/
            Headers: Authorization: Bearer <token>
            Body: {
                "translations": {
                    "en": {
                        "name": "Caesar Salad",
                        "description": "Fresh romaine with Caesar dressing"
                    },
                    "es": {
                        "name": "Ensalada César",
                        "description": "Lechuga romana fresca con aderezo César"
                    }
                },
                "price": "8.99",
                "stock": 30,
                "available": true,
                "categories": [2],
                "ingredients": [1, 5, 7]
            }

    Notes:
        - Only available products are shown by default (available=True filter).
        - Uses ProductSerializerGet for read operations (list, retrieve).
        - Uses ProductSerializerPost for write operations (create, update).
        - Supports filtering by multiple categories or ingredients.
        - Search is performed across all available translations.
        - Read operations are public; write operations require authentication.
        - Supports django-parler for multilingual fields.
        - Includes timestamp tracking (created_at, updated_at).
    """

    queryset = Product.objects.filter(available=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['available', 'categories', 'ingredients']
    ordering_fields = ['price', 'stock', 'created_at', 'updated_at']
    search_fields = ['translations__name', 'translations__description']

    def get_serializer_class(self) -> type[Serializer]:
        """Return the appropriate serializer class based on the action.

        Returns:
            ProductSerializerGet for list and retrieve actions (read operations).
            ProductSerializerPost for create, update, and delete actions
                (write operations).
        """
        if self.action in ['list', 'retrieve']:
            return ProductSerializerGet
        return ProductSerializerPost
    