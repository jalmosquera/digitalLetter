from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from apps.categories.models import Category
from apps.ingredients.models import Ingredients

class Products(TranslatableModel):
    '''Model definition for Products.'''
    translations = TranslatedFields(
        name = models.CharField(max_length=100),
        description = models.TextField(blank=True, null=True),
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='Products/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='Products', blank=True)
    ingredients = models.ManyToManyField(Ingredients, related_name='Products', blank=True)  # ✅ ingredientes
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Products {self.pk}"

    class Meta:
        verbose_name_plural = "Products"



