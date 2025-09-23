from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Plates 

@admin.register(Plates)
class ProductsAdmin(TranslatableAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    
