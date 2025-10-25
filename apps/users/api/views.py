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
    """ViewSet for managing employee accounts with role-based access control.

    This viewset provides CRUD operations for employee user accounts. Only
    staff members can create, update, or delete employees. Both staff and
    employees can list employee accounts.

    Attributes:
        queryset: QuerySet filtered to users with role='employe'.
        serializer_class: SerializerEmploye for all operations.
        permission_classes: IsStaff by default (can be overridden per action).

    Endpoints:
        GET /api/employees/
            List all employee accounts.
            Returns: List of employees with their details.
            Permissions: IsStaffOrEmploye (staff and employees can view).

        POST /api/employees/
            Create a new employee account.
            Request Body: SerializerEmploye schema with password.
            Returns: Created employee details (201 Created).
            Permissions: IsStaff (staff only).

        GET /api/employees/{id}/
            Retrieve a specific employee by ID.
            Returns: Employee details.
            Permissions: IsStaff (staff only).

        PUT /api/employees/{id}/
            Fully update an employee account.
            Request Body: SerializerEmploye schema.
            Returns: Updated employee details.
            Permissions: IsStaff (staff only).

        PATCH /api/employees/{id}/
            Partially update an employee account.
            Request Body: Partial SerializerEmploye schema.
            Returns: Updated employee details.
            Permissions: IsStaff (staff only).

        DELETE /api/employees/{id}/
            Delete an employee account.
            Returns: 204 No Content on success.
            Permissions: IsStaff (staff only).

    Examples:
        Create an employee:
            POST /api/employees/
            Headers: Authorization: Bearer <staff_token>
            Body: {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "SecurePass123!",
                "first_name": "John",
                "last_name": "Doe",
                "role": "employe"
            }

        List employees:
            GET /api/employees/
            Headers: Authorization: Bearer <token>
            Response: [
                {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "role": "employe",
                    "first_name": "John",
                    "last_name": "Doe"
                }
            ]

    Notes:
        - Password is hashed before saving using Django's set_password method.
        - Role is automatically set to 'employe' by the serializer.
        - List operation accessible by both staff and employees.
        - All other operations restricted to staff only.
        - Uses custom permission classes: IsStaff and IsStaffOrEmploye.
    """

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
    """ViewSet for managing client accounts and self-registration.

    This viewset provides CRUD operations for client user accounts. Clients
    can self-register through the create endpoint. Uses default DRF permissions
    which can be configured at the project level.

    Attributes:
        queryset: QuerySet filtered to users with role='client'.
        serializer_class: SerializerClients for all operations.

    Endpoints:
        GET /api/clients/
            List all client accounts.
            Returns: List of clients with their details.
            Permissions: Default DRF permissions.

        POST /api/clients/
            Register a new client account (public registration).
            Request Body: SerializerClients schema with password.
            Returns: Created client details (201 Created).
            Permissions: Default DRF permissions (typically AllowAny).

        GET /api/clients/{id}/
            Retrieve a specific client by ID.
            Returns: Client details.
            Permissions: Default DRF permissions.

        PUT /api/clients/{id}/
            Fully update a client account.
            Request Body: SerializerClients schema.
            Returns: Updated client details.
            Permissions: Default DRF permissions.

        PATCH /api/clients/{id}/
            Partially update a client account.
            Request Body: Partial SerializerClients schema.
            Returns: Updated client details.
            Permissions: Default DRF permissions.

        DELETE /api/clients/{id}/
            Delete a client account.
            Returns: 204 No Content on success.
            Permissions: Default DRF permissions.

    Examples:
        Register a new client:
            POST /api/clients/
            Body: {
                "username": "maria_garcia",
                "email": "maria@example.com",
                "password": "SecurePass456!",
                "first_name": "Maria",
                "last_name": "Garcia",
                "phone": "+1234567890"
            }
            Response: {
                "id": 5,
                "username": "maria_garcia",
                "email": "maria@example.com",
                "role": "client",
                "first_name": "Maria",
                "last_name": "Garcia",
                "phone": "+1234567890"
            }

        List all clients:
            GET /api/clients/
            Response: [
                {
                    "id": 5,
                    "username": "maria_garcia",
                    "email": "maria@example.com",
                    "role": "client",
                    "first_name": "Maria",
                    "last_name": "Garcia"
                }
            ]

        Update client information:
            PATCH /api/clients/5/
            Body: {
                "phone": "+0987654321"
            }

    Notes:
        - Password is hashed before saving using Django's set_password method.
        - Role is automatically set to 'client' by the serializer.
        - No custom permissions defined; uses Django REST Framework defaults.
        - Commonly used for customer self-registration in the system.
        - Password field should be write-only (not returned in responses).
    """

    queryset = User.objects.filter(role="client")
    serializer_class = SerializerClients

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
    """Read-only ViewSet for listing and retrieving users with role-based access.

    This viewset provides filtered user listing based on the requesting user's
    role. Staff can view all users, employees can view clients and themselves,
    and other users have no access.

    Attributes:
        permission_classes: IsStaffOrEmploye (staff and employees only).
        serializer_class: UserListSerializer for all operations.

    Endpoints:
        GET /api/users/
            List users with role-based filtering.
            Returns: List of users based on requester's role.
            Permissions: IsStaffOrEmploye (staff and employees only).
            Filtering Logic:
                - Staff: See all users in the system
                - Employees: See all clients + themselves
                - Others: No access (403 Forbidden)

        GET /api/users/{id}/
            Retrieve a specific user by ID.
            Returns: User details if accessible based on role.
            Permissions: IsStaffOrEmploye (staff and employees only).

    Examples:
        List users as staff:
            GET /api/users/
            Headers: Authorization: Bearer <staff_token>
            Response: [
                {"id": 1, "username": "admin", "role": "staff", ...},
                {"id": 2, "username": "john_doe", "role": "employe", ...},
                {"id": 3, "username": "maria", "role": "client", ...}
            ]

        List users as employee:
            GET /api/users/
            Headers: Authorization: Bearer <employee_token>
            Response: [
                {"id": 2, "username": "john_doe", "role": "employe", ...},
                {"id": 3, "username": "maria", "role": "client", ...},
                {"id": 4, "username": "pedro", "role": "client", ...}
            ]

        Retrieve specific user:
            GET /api/users/3/
            Headers: Authorization: Bearer <token>
            Response: {
                "id": 3,
                "username": "maria",
                "email": "maria@example.com",
                "role": "client",
                "first_name": "Maria",
                "last_name": "Garcia"
            }

    Notes:
        - Read-only viewset: no create, update, or delete operations.
        - Staff users see all users regardless of role.
        - Employees see only clients and their own profile.
        - Uses Q objects for complex queryset filtering.
        - Returns empty queryset for unauthorized roles.
        - Additional authorization check in list method for safety.
    """

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
    """API view for managing the authenticated user's own profile.

    This view allows users to retrieve and update their own profile information.
    Users can only access and modify their own data, not other users' profiles.

    Attributes:
        permission_classes: IsAuthenticated (any authenticated user).

    Endpoints:
        GET /api/me/
            Retrieve the current user's profile information.
            Returns: Current user's profile data.
            Permissions: IsAuthenticated (any authenticated user).

        PATCH /api/me/
            Update the current user's profile information.
            Request Body: Partial UserListSerializer schema.
            Returns: Updated profile data.
            Permissions: IsAuthenticated (any authenticated user).

    Examples:
        Get current user profile:
            GET /api/me/
            Headers: Authorization: Bearer <token>
            Response: {
                "id": 5,
                "username": "maria_garcia",
                "email": "maria@example.com",
                "role": "client",
                "first_name": "Maria",
                "last_name": "Garcia",
                "phone": "+1234567890"
            }

        Update current user profile:
            PATCH /api/me/
            Headers: Authorization: Bearer <token>
            Body: {
                "first_name": "María",
                "phone": "+0987654321"
            }
            Response: {
                "id": 5,
                "username": "maria_garcia",
                "email": "maria@example.com",
                "role": "client",
                "first_name": "María",
                "last_name": "Garcia",
                "phone": "+0987654321"
            }

    Notes:
        - Users can only view and update their own profile.
        - Partial updates are supported (PATCH method).
        - Cannot change password through this endpoint (use /change-password/).
        - Cannot change role or sensitive fields through this endpoint.
        - Automatically gets user from request.user (JWT token).
    """

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
    """API view for changing the authenticated user's password.

    This view allows authenticated users to change their own password by
    providing their current password and a new password. Validates the old
    password before allowing the change.

    Attributes:
        permission_classes: IsAuthenticated (any authenticated user).

    Endpoints:
        POST /api/change-password/
            Change the current user's password.
            Request Body: ChangePasswordSerializer schema with old_password
                and new_password fields.
            Returns: Success message (200) or error (400).
            Permissions: IsAuthenticated (any authenticated user).

    Examples:
        Change password:
            POST /api/change-password/
            Headers: Authorization: Bearer <token>
            Body: {
                "old_password": "OldPass123!",
                "new_password": "NewSecurePass456!"
            }
            Response: {
                "detail": "Password updated successfully."
            }

        Incorrect old password:
            POST /api/change-password/
            Body: {
                "old_password": "WrongPassword",
                "new_password": "NewSecurePass456!"
            }
            Response (400): {
                "old_password": "Current password is incorrect."
            }

        Invalid new password:
            POST /api/change-password/
            Body: {
                "old_password": "OldPass123!",
                "new_password": "weak"
            }
            Response (400): {
                "new_password": ["Password is too short.", ...]
            }

    Notes:
        - Requires current password verification for security.
        - New password must meet Django's password validation requirements.
        - Password is hashed before saving using set_password method.
        - User must be authenticated to access this endpoint.
        - After password change, existing tokens remain valid (consider
          implementing token invalidation if using JWT).
    """

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