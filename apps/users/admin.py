"""Django admin configuration for the users application.

This module configures the Django admin interface for user-related models.
Currently, no custom admin classes are registered, but this file is preserved
for future admin customizations.

Notes:
    - No models are currently registered in this admin module.
    - User authentication is handled through Django's built-in User model
      or a custom User model defined in apps.users.models.
    - Custom permission classes are defined in apps.users.permisionsUsers.
    - Future admin customizations for user management can be added here.

See Also:
    - apps.users.models for User model definition
    - apps.users.permisionsUsers for custom permission classes
    - Django admin documentation for user management
"""

from django.contrib import admin

# Register your models here.
