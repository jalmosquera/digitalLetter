from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from apps.products.models import Products
from apps.products.api.serializer import ProductSerializerPost, ProductSerializerGet
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

@extend_schema_view(
    list=extend_schema(
        tags=['products'],
        responses=ProductSerializerGet(many=True),
    ),
    create=extend_schema(
        tags=['products'],
        request=ProductSerializerPost,
        responses={201: ProductSerializerGet, 400: OpenApiResponse(description='Invalid data')},
    ),
    retrieve=extend_schema(
        tags=['products'],
        responses={200: ProductSerializerGet, 404: OpenApiResponse(description='Not found')},
    ),
    update=extend_schema(
        tags=['products'],
        request=ProductSerializerPost,
        responses={200: ProductSerializerGet, 400: OpenApiResponse(description='Invalid data')},
    ),
    partial_update=extend_schema(
        tags=['products'],
        request=ProductSerializerPost,
        responses={200: ProductSerializerGet, 400: OpenApiResponse(description='Invalid data')},
    ),
    destroy=extend_schema(
        tags=['products'],
        responses={204: OpenApiResponse(description='Deleted')},
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.filter(available=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['available', 'categories', 'ingredients']
    ordering_fields = ['price', 'stock', 'created_at', 'updated_at']
    search_fields = ['translations__name', 'translations__description']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductSerializerGet
        return ProductSerializerPost
    