from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Ingredients

@admin.register(Ingredients)
class IngredientsAdmin(TranslatableAdmin):
    list_display = ('name',)