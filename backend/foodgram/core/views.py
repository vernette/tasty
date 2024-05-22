from rest_framework import viewsets

from core.serializers import IngredientSerializer, TagSerializer
from core.models import Ingredient, Tag


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
