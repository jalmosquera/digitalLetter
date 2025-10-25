"""Company API views module.

This module provides REST API viewsets for managing company information in
the digital menu system. Company data includes business details such as name,
address, contact information, and operating hours.

Typical usage example:
    GET /api/company/ - List all companies
    POST /api/company/ - Create a new company
    GET /api/company/{id}/ - Retrieve company details
    PUT /api/company/{id}/ - Update company information
    PATCH /api/company/{id}/ - Partially update company information
    DELETE /api/company/{id}/ - Delete a company
"""

from typing import Any

from rest_framework import viewsets
from rest_framework.serializers import Serializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response

from apps.company.models import Company
from apps.company.api.serializers import CompanySerializer


@extend_schema_view(
    list=extend_schema(
        tags=['company'],
        responses=CompanySerializer(many=True),
    ),
    create=extend_schema(
        tags=['company'],
        request=CompanySerializer,
        responses={
            201: CompanySerializer,
            400: Response({'detail': 'Invalid data'}),
        },
    ),
    retrieve=extend_schema(
        tags=['company'],
        responses={
            200: CompanySerializer,
            404: Response({'detail': 'Not found'}),
        },
    ),
    update=extend_schema(
        tags=['company'],
        request=CompanySerializer,
        responses={
            200: CompanySerializer,
            400: Response({'detail': 'Invalid data'}),
        },
    ),
    partial_update=extend_schema(
        tags=['company'],
        request=CompanySerializer,
        responses={
            200: CompanySerializer,
            400: Response({'detail': 'Invalid data'}),
        },
    ),
    destroy=extend_schema(
        tags=['company'],
        responses={204: Response({'detail': 'Deleted successfully'})},
    ),
)
class CompanyView(viewsets.ModelViewSet):
    """ViewSet for managing company information and business details.

    This viewset provides full CRUD operations for company records. It manages
    business information such as company name, address, contact details,
    operating hours, and other relevant business metadata for the digital
    menu system.

    Attributes:
        queryset: QuerySet containing all Company objects.
        serializer_class: CompanySerializer for all operations.

    Endpoints:
        GET /api/company/
            List all companies in the system.
            Returns: List of companies with full details.
            Permissions: Default DRF permissions (typically authenticated).

        POST /api/company/
            Create a new company record.
            Request Body: CompanySerializer schema.
            Returns: Created company details (201 Created).
            Permissions: Default DRF permissions (typically authenticated).

        GET /api/company/{id}/
            Retrieve a specific company by ID.
            Returns: Company details including all business information.
            Permissions: Default DRF permissions (typically authenticated).

        PUT /api/company/{id}/
            Fully update a company's information.
            Request Body: Complete CompanySerializer schema.
            Returns: Updated company details.
            Permissions: Default DRF permissions (typically authenticated).

        PATCH /api/company/{id}/
            Partially update a company's information.
            Request Body: Partial CompanySerializer schema.
            Returns: Updated company details.
            Permissions: Default DRF permissions (typically authenticated).

        DELETE /api/company/{id}/
            Delete a company record.
            Returns: 204 No Content on success.
            Permissions: Default DRF permissions (typically authenticated).

    Examples:
        List all companies:
            GET /api/company/
            Response: [
                {
                    "id": 1,
                    "name": "Pizza Palace",
                    "address": "123 Main St, City",
                    "phone": "+1234567890",
                    "email": "contact@pizzapalace.com",
                    "opening_hours": "Mon-Sun: 10:00-22:00",
                    "description": "Best pizza in town"
                }
            ]

        Create a company:
            POST /api/company/
            Headers: Authorization: Bearer <token>
            Body: {
                "name": "Burger House",
                "address": "456 Oak Ave, City",
                "phone": "+0987654321",
                "email": "info@burgerhouse.com",
                "opening_hours": "Mon-Sat: 11:00-21:00",
                "description": "Gourmet burgers and craft beers"
            }

        Update company information:
            PATCH /api/company/1/
            Headers: Authorization: Bearer <token>
            Body: {
                "phone": "+1234567899",
                "opening_hours": "Mon-Sun: 09:00-23:00"
            }

        Retrieve company details:
            GET /api/company/1/
            Response: {
                "id": 1,
                "name": "Pizza Palace",
                "address": "123 Main St, City",
                "phone": "+1234567899",
                "email": "contact@pizzapalace.com",
                "opening_hours": "Mon-Sun: 09:00-23:00",
                "description": "Best pizza in town",
                "logo": "https://example.com/media/logos/pizza_palace.png",
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-20T14:45:00Z"
            }

    Notes:
        - Typically, a system will have only one company record.
        - All fields are managed through the CompanySerializer.
        - May include additional fields such as logo, social media links, etc.
        - No custom permissions defined; uses Django REST Framework defaults.
        - Consider implementing object-level permissions for multi-tenant systems.
        - Business hours can be stored in various formats (JSON, text, etc.).
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
