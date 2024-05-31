from django.urls import path, include
from rest_framework.routers import DefaultRouter

from favorites.views import RecipeFavoriteAPIView
from core.views import IngredientViewSet, TagViewSet, RecipeViewSet


router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:id>/favorite/', RecipeFavoriteAPIView.as_view(), name='recipe-favorite'),
]
