from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Products 

@admin.register(Products)
class ProductsAdmin(TranslatableAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    
