from django.urls import path, include
from rest_framework.routers import DefaultRouter

from favorites.views import RecipeFavoriteAPIView
from shopping_list.views import RecipeShoppingCartAPIView, DownloadShoppingCartTXTView, DownloadShoppingCartJSONView
from core.views import IngredientViewSet, TagViewSet, RecipeViewSet


router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCartTXTView.as_view(), name='download-shopping-cart'),
    path('recipes/download_shopping_cart_json/', DownloadShoppingCartJSONView.as_view(), name='download-shopping-cart-json'),
    path('recipes/<int:id>/favorite/', RecipeFavoriteAPIView.as_view(), name='recipe-favorite'),
    path('recipes/<int:id>/shopping_cart/', RecipeShoppingCartAPIView.as_view(), name='recipe-shopping-cart'),
    path('', include(router.urls)),
]
