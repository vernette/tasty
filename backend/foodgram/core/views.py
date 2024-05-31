from shortener.models import Url
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from core.serializers import IngredientSerializer, TagSerializer, RecipeSerializer
from core.models import Ingredient, Tag, Recipe


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        long_url = request.build_absolute_uri(f'/recipes/{recipe.pk}/')
        short_url, _ = Url.objects.get_or_create(long_url=long_url)
        short_link = request.build_absolute_uri(f'/s/{short_url.short_id}/')
        return Response({'short-link': short_link}, status=status.HTTP_200_OK)