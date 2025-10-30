"""Users API views module.

This module provides REST API views and viewsets for user management in the
digital menu system. It handles employee registration, client registration,
user listing, profile management, and password changes with role-based
access control.

Typical usage example:
    # Employee Management (Staff only)
    GET /api/employees/ - List all employees
    POST /api/employees/ - Create a new employee account
    GET /api/employees/{id}/ - Retrieve employee details
    PUT /api/employees/{id}/ - Update employee information
    DELETE /api/employees/{id}/ - Delete employee account

    # Client Management
    GET /api/clients/ - List all clients
    POST /api/clients/ - Register a new client account
    GET /api/clients/{id}/ - Retrieve client details
    PUT /api/clients/{id}/ - Update client information

    # User Management
    GET /api/users/ - List users (staff sees all, employees see clients)
    GET /api/users/{id}/ - Retrieve user details

    # Profile Management
    GET /api/me/ - Get current user profile
    PATCH /api/me/ - Update current user profile

    # Password Management
    POST /api/change-password/ - Change user password
"""

from typing import Any

from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.request import Request
from django.db.models import Q, QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.users.permisionsUsers import IsStaff, IsBoss, IsStaffOrEmploye
from apps.users.models import User
from apps.users.api.serializers import (
    SerializerClients,
    SerializerEmploye,
    UserListSerializer,
    ChangePasswordSerializer
)


@extend_schema_view(
    list=extend_schema(
        tags=["employee"],
        description="List all employees in the system",
    ),
    create=extend_schema(
        tags=["employee"],
        description="Create a new employee account",
        request=SerializerEmploye,
        responses={
            201: SerializerEmploye,
            400: Response({"description": "Invalid data provided"}),
            403: Response({"description": "Permission denied"}),
        },
    ),
    retrieve=extend_schema(
        tags=["employee"],
        description="Retrieve a specific employee by ID",
        responses={
            200: SerializerEmploye,
            404: Response({"description": "Employee not found"}),
        },
    ),
    update=extend_schema(
        tags=["employee"],
        description="Update a specific employee by ID",
        request=SerializerEmploye,
        responses={
            200: SerializerEmploye,
            400: Response({"description": "Invalid data provided"}),
            404: Response({"description": "Employee not found"}),
        },
    ),
    partial_update=extend_schema(
        tags=["employee"],
        description="Partially update a specific employee by ID",
        request=SerializerEmploye,
        responses={
            200: SerializerEmploye,
            400: Response({"description": "Invalid data provided"}),
            404: Response({"description": "Employee not found"}),
        },
    ),
    destroy=extend_schema(
        tags=["employee"],
        description="Delete a specific employee by ID",
        responses={
            204: Response({"description": "Employee deleted successfully"}),
            404: Response({"description": "Employee not found"}),
        },
    ),
)
class RegisterEmploye(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="employe")
    serializer_class = SerializerEmploye
    permission_classes = [IsStaff]

    def get_permissions(self) -> list[BasePermission]:
        """Return appropriate permissions based on the action.

        Returns:
            List of permission instances. IsStaff for create/update/delete,
            IsStaffOrEmploye for list operations.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaff()]
        elif self.action == 'list':
            return [IsStaffOrEmploye()]
        return super().get_permissions()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new employee account with hashed password.

        Validates the employee data, creates the user, and hashes the password
        before saving to the database.

        Args:
            request: The HTTP request containing employee data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response with created employee data (201) or validation errors (400).

        Notes:
            Password must be provided in plain text and will be hashed using
            Django's set_password method before saving.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get("password")
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        tags=["clients"],
        description="List all client accounts in the system",
    ),
    create=extend_schema(
        tags=["clients"],
        description="Register a new client account",
        request=SerializerClients,
        responses={
            201: SerializerClients,
            400: Response({"description": "Invalid data provided"}),
        },
    ),
    retrieve=extend_schema(
        tags=["clients"],
        description="Retrieve a specific client by ID",
        responses={
            200: SerializerClients,
            404: Response({"description": "Client not found"}),
        },
    ),
    update=extend_schema(
        tags=["clients"],
        description="Update a specific client by ID",
        request=SerializerClients,
        responses={
            200: SerializerClients,
            400: Response({"description": "Invalid data provided"}),
            404: Response({"description": "Client not found"}),
        },
    ),
    partial_update=extend_schema(
        tags=["clients"],
        description="Partially update a specific client by ID",
        request=SerializerClients,
        responses={
            200: SerializerClients,
            400: Response({"description": "Invalid data provided"}),
            404: Response({"description": "Client not found"}),
        },
    ),
    destroy=extend_schema(
        tags=["clients"],
        description="Delete a specific client by ID",
        responses={
            204: Response({"description": "Client deleted successfully"}),
            404: Response({"description": "Client not found"}),
        },
    ),
)
class RegisterClients(viewsets.ModelViewSet):
    queryset = User.objects.filter(role="client")
    serializer_class = SerializerClients
    permission_classes = [AllowAny]  # Allow public registration

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Register a new client account with hashed password.

        Validates the client data, creates the user, and hashes the password
        before saving to the database. This endpoint typically allows public
        access for self-registration.

        Args:
            request: The HTTP request containing client registration data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response with created client data (201) or validation errors (400).

        Notes:
            Password must be provided in plain text and will be hashed using
            Django's set_password method before saving. The password field
            should not be returned in the response.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            password = request.data.get("password")
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        tags=["users"],
        description="List users with role-based filtering",
        responses={200: UserListSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["users"],
        description="Retrieve a specific user by ID",
        responses={
            200: UserListSerializer,
            404: Response({"description": "User not found"}),
        },
    ),
)
class UsersListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsStaffOrEmploye]
    serializer_class = UserListSerializer

    def get_queryset(self) -> QuerySet[User]:
        """Return filtered queryset based on the requesting user's role.

        Returns:
            QuerySet of User objects filtered by role:
            - Staff: All users
            - Employees: Clients + self
            - Others: Empty queryset
        """
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        elif user.role == "employe":
            return User.objects.filter(Q(role="client") | Q(id=user.id))
        return User.objects.none()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List users with additional authorization check.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response with user list or 403 Forbidden if not authorized.

        Notes:
            Provides an additional security layer beyond permission classes
            to ensure only staff and employees can list users.
        """
        if not (request.user.is_staff or request.user.role == "employe"):
            return Response({"detail": "Not authorized."}, status=403)
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=["profile"],
    methods=["GET"],
    description="Get current user profile information",
    responses={200: UserListSerializer},
)
@extend_schema(
    tags=["profile"],
    methods=["PATCH"],
    description="Update current user profile information",
    request=UserListSerializer,
    responses={
        200: UserListSerializer,
        400: Response({"description": "Invalid data provided"}),
    },
)
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Retrieve the authenticated user's profile information.

        Args:
            request: The HTTP request containing authenticated user.

        Returns:
            Response with the user's profile data.
        """
        user = request.user
        serializer = UserListSerializer(user)
        return Response(serializer.data)

    def patch(self, request: Request) -> Response:
        """Update the authenticated user's profile information.

        Args:
            request: The HTTP request containing profile update data.

        Returns:
            Response with updated profile data (200) or validation errors (400).

        Notes:
            Supports partial updates. Only provided fields will be updated.
        """
        user = request.user
        serializer = UserListSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["profile"],
    methods=["POST"],
    description="Change user password",
    request=ChangePasswordSerializer,
    responses={
        200: Response({"description": "Password updated successfully"}),
        400: Response({"description": "Invalid password or validation error"}),
    },
)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Change the authenticated user's password.

        Validates the old password, then updates to the new password if valid.

        Args:
            request: The HTTP request containing old and new passwords.

        Returns:
            Response with success message (200) or error details (400).

        Notes:
            Old password must be correct, and new password must pass Django's
            password validators.
        """
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": "Current password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {"detail": "Password updated successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)