"""User serializers for REST API operations.

This module provides serializers for the User model, supporting role-based user
creation, profile management, and password changes through Django REST Framework.
"""

from typing import Any, Dict
from rest_framework import serializers
from ..models import User


class SerializerClients(serializers.ModelSerializer):
    """Serializer for creating client user accounts.

    Handles user registration for client role accounts. Automatically sets
    the user role to 'client' (default in User model). Used for customer
    registration endpoints.

    Meta:
        model: User model this serializer is based on.
        fields: Includes username, email, name, and password fields only.

    Example:
        >>> # Create a new client account
        >>> data = {
        ...     'username': 'customer1',
        ...     'email': 'customer@example.com',
        ...     'name': 'John Customer',
        ...     'password': 'securepass123'
        ... }
        >>> serializer = SerializerClients(data=data)
        >>> if serializer.is_valid():
        ...     user = serializer.save()
        ...     # Password will be hashed automatically
        ...     user.role  # 'client' (default)
        'client'

    Note:
        - Password field should be write-only in production (consider adding write_only=True)
        - User role defaults to 'client' as defined in User model
        - Password is stored as plain text without hashing (security issue - needs fixing)
        - Consider using create() method to hash password with user.set_password()
    """

    class Meta:
        """Meta options for SerializerClients."""

        model = User
        fields = ['username', 'email', 'name', 'password']


class SerializerEmploye(serializers.ModelSerializer):
    """Serializer for creating employee user accounts.

    Handles user registration for employee role accounts. Automatically sets
    the user role to 'employe' during validation. Used for staff member
    registration by administrators.

    Meta:
        model: User model this serializer is based on.
        fields: Includes username, name, email, and password fields only.

    Example:
        >>> # Create a new employee account
        >>> data = {
        ...     'username': 'staff1',
        ...     'name': 'Jane Staff',
        ...     'email': 'staff@example.com',
        ...     'password': 'staffpass123'
        ... }
        >>> serializer = SerializerEmploye(data=data)
        >>> if serializer.is_valid():
        ...     user = serializer.save()
        ...     user.role  # 'employe' (set automatically)
        'employe'

    Note:
        - Role is automatically set to 'employe' in validate() method
        - Password field should be write-only in production
        - Password is stored as plain text without hashing (security issue - needs fixing)
        - Consider using create() method to hash password with user.set_password()
    """

    class Meta:
        """Meta options for SerializerEmploye."""

        model = User
        fields = ['username', 'name', 'email', 'password']

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set employee role for the user.

        Automatically assigns 'employe' role to the user data during validation,
        ensuring all users created with this serializer have employee permissions.

        Args:
            data: Dictionary containing validated field data (username, name,
                email, password).

        Returns:
            Dict with original data plus 'role' field set to 'employe'.

        Example:
            >>> data = {
            ...     'username': 'newstaff',
            ...     'name': 'New Staff',
            ...     'email': 'newstaff@example.com',
            ...     'password': 'pass123'
            ... }
            >>> validated_data = serializer.validate(data)
            >>> validated_data['role']
            'employe'
        """
        data['role'] = 'employe'
        return data


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating user profile information.

    Handles GET and PATCH requests for user data, returning or updating
    profile information including contact details and role. Excludes sensitive
    fields like password. Used for user list endpoints and profile management.

    Meta:
        model: User model this serializer is based on.
        fields: Includes id, username, name, email, role, image, address,
            location, province, and phone fields.

    Example:
        >>> # Retrieve user profile
        >>> user = User.objects.get(id=1)
        >>> serializer = UserListSerializer(user)
        >>> serializer.data
        {
            'id': 1,
            'username': 'customer1',
            'name': 'John Customer',
            'email': 'customer@example.com',
            'role': 'client',
            'image': '/media/avatar/default.jpg',
            'address': '123 Main St',
            'location': 'New York',
            'province': 'NY',
            'phone': '+1234567890'
        }
        >>>
        >>> # Update user profile
        >>> data = {
        ...     'address': '456 Oak Ave',
        ...     'phone': '+0987654321'
        ... }
        >>> serializer = UserListSerializer(user, data=data, partial=True)
        >>> if serializer.is_valid():
        ...     user = serializer.save()
        >>>
        >>> # List all users
        >>> users = User.objects.all()
        >>> serializer = UserListSerializer(users, many=True)
        >>> serializer.data  # Returns list of user profiles

    Note:
        - Excludes password and other sensitive authentication fields
        - Suitable for both retrieval and partial updates
        - Image field returns URL path to user avatar
        - Role field is included but should be read-only for non-admin users
    """

    class Meta:
        """Meta options for UserListSerializer."""

        model = User
        fields = ['id', 'username', 'name', 'email', 'role', 'image', 'address', 'location', 'province', 'phone']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for handling user password change requests.

    Validates password change requests by ensuring the new password is
    confirmed correctly. Does not validate the old password (should be done
    in the view). Used for authenticated user password change endpoints.

    Attributes:
        old_password (CharField): User's current password for verification.
        new_password (CharField): New password to set for the user.
        new_password_confirm (CharField): Confirmation of the new password.

    Example:
        >>> # Change password
        >>> data = {
        ...     'old_password': 'oldpass123',
        ...     'new_password': 'newpass456',
        ...     'new_password_confirm': 'newpass456'
        ... }
        >>> serializer = ChangePasswordSerializer(data=data)
        >>> if serializer.is_valid():
        ...     # In view: verify old_password and set new_password
        ...     user.set_password(serializer.validated_data['new_password'])
        ...     user.save()
        >>>
        >>> # Validation error example
        >>> data = {
        ...     'old_password': 'oldpass123',
        ...     'new_password': 'newpass456',
        ...     'new_password_confirm': 'different_password'
        ... }
        >>> serializer = ChangePasswordSerializer(data=data)
        >>> serializer.is_valid()
        False
        >>> serializer.errors
        {'non_field_errors': ['Las contraseñas no coinciden.']}

    Note:
        - Does not verify old_password (must be done in view with check_password())
        - Does not enforce password strength requirements
        - Error message is in Spanish ("Las contraseñas no coinciden.")
        - Consider adding password strength validation
        - Should be used with authentication required
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data: Dict[str, str]) -> Dict[str, str]:
        """Validate that new password and confirmation match.

        Ensures the new password and its confirmation are identical before
        allowing the password change to proceed.

        Args:
            data: Dictionary containing old_password, new_password, and
                new_password_confirm fields.

        Returns:
            Dict with validated password data if confirmation matches.

        Raises:
            ValidationError: If new_password and new_password_confirm do not match.

        Example:
            >>> data = {
            ...     'old_password': 'oldpass',
            ...     'new_password': 'newpass',
            ...     'new_password_confirm': 'newpass'
            ... }
            >>> validated_data = serializer.validate(data)
            >>> # No error, passwords match
            >>>
            >>> data['new_password_confirm'] = 'different'
            >>> serializer.validate(data)
            ValidationError: Las contraseñas no coinciden.
        """
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data