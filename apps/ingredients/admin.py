from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(TranslatableAdmin):
    list_display = ('name',)