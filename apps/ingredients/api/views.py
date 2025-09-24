from rest_framework import viewsets
from apps.ingredients.models import Ingredients
from apps.ingredients.api.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint para crear, listar, actualizar y borrar ingredientes.
    Incluye soporte de traducciones vía django-parler.
    """
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
