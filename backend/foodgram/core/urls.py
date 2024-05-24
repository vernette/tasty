from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import IngredientViewSet, TagViewSet, RecipeViewSet


router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
