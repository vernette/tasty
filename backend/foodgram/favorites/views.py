from core.models import Recipe
from shopping_list.views import BaseRecipeAPIView
from favorites.models import Favorite


class RecipeFavoriteAPIView(BaseRecipeAPIView):
    main_model = Recipe
    related_model = Favorite
    create_message = 'Рецепт уже в избранном.'
    not_found_message = 'Рецепта нет в избранном.'
