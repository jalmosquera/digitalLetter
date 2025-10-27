# core/production.py
"""
Production settings for Railway deployment.
To use: Set environment variable DJANGO_SETTINGS_MODULE=core.production
"""

from .settings import *
import dj_database_url
from decouple import config
import os

# Override DEBUG for production
DEBUG = False

# Get allowed hosts from environment variable
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='.railway.app').split(',')

# Database configuration with Railway PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files configuration for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Remove STATICFILES_DIRS in production (it conflicts with STATIC_ROOT)
STATICFILES_DIRS = []

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS configuration from environment
cors_origins = config('CORS_ALLOWED_ORIGINS', default='')
if cors_origins:
    CORS_ALLOWED_ORIGINS = cors_origins.split(',')
else:
    CORS_ALLOWED_ORIGINS = []

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Get SECRET_KEY from environment
SECRET_KEY = config('SECRET_KEY')

# Language code from environment
LANGUAGE_CODE = config('LANGUAGE_CODE', default='es')
