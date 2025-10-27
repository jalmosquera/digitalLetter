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
    