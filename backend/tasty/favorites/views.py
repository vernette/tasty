from core.models import Recipe
from shopping_list.views import BaseRecipeAPIView
from favorites.models import Favorite
from tasty.constants import FAVORITES_NOT_FOUND, FAVORITES_ALREADY_EXISTS


class RecipeFavoriteAPIView(BaseRecipeAPIView):
    main_model = Recipe
    related_model = Favorite
    exists_message = FAVORITES_ALREADY_EXISTS
    not_found_message = FAVORITES_NOT_FOUND
