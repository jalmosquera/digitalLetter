from django.db import models
from parler.models import TranslatableModel,TranslatedFields



class Ingredients(TranslatableModel):
    """Should be all ingredients."""
    translations = TranslatedFields(  # ✅ corregido
        name = models.CharField('Name', max_length=50)
    )
    icon = models.CharField('Icon', max_length=50,null=True,blank=True)
    
    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Ingredients {self.pk}"

