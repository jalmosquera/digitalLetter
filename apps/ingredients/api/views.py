from rest_framework import viewsets
from apps.ingredients.models import Ingredient
from apps.ingredients.api.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint para crear, listar, actualizar y borrar ingredientes.
    Incluye soporte de traducciones vía django-parler.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
