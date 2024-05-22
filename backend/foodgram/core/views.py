from rest_framework import viewsets

from core.serializers import IngredientSerializer
from core.models import Ingredient


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
