from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from shortener.models import Url

from core.models import Ingredient, Recipe, Tag
from core.serializers import (
    IngredientSerializer, RecipeSerializer, TagSerializer
)

from core.filters import IngredientFilter, RecipeFilter
from core.mixins import ReadOnlyOrAdminMixin
from core.pagination import CustomPageNumberPagination
from core.permissions import (
    IsAuthenticatedAndReadOnly, IsOwnerOrAdminOrReadOnly
)


class IngredientViewSet(ReadOnlyOrAdminMixin, viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyOrAdminMixin, viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [
        IsOwnerOrAdminOrReadOnly,
        IsAuthenticatedAndReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        long_url = request.build_absolute_uri(f'/recipes/{recipe.pk}/')
        short_url, _ = Url.objects.get_or_create(long_url=long_url)
        short_link = request.build_absolute_uri(f'/s/{short_url.short_id}/')
        return Response(
            {'short-link': short_link},
            status=status.HTTP_200_OK
        )
