from rest_framework import viewsets
from apps.company.models import Company
from apps.company.api.serializers import CompanySerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response

@extend_schema_view(
    list=extend_schema(
        tags=['company'],
        responses=CompanySerializer(many=True),
    ),
    create=extend_schema(
        tags=['company'],
        request=CompanySerializer,
        responses={201: CompanySerializer, 400: Response({'detail': 'Invalid data'})},
    ),
    retrieve=extend_schema(
        tags=['company'],
        responses={200: CompanySerializer, 404: Response({'detail': 'Not found'})},
    ),
    update=extend_schema(
        tags=['company'],
        request=CompanySerializer,
        responses={200: CompanySerializer, 400: Response({'detail': 'Invalid data'})},
    ),
    partial_update=extend_schema(
        tags=['company'],
        request=CompanySerializer,
        responses={200: CompanySerializer, 400: Response({'detail': 'Invalid data'})},
    ),
    destroy=extend_schema(
        tags=['company'],
    ),
)
class CompanyView(viewsets.ModelViewSet):
    """
    ViewSet for Company model.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
