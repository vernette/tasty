import json
from collections import defaultdict
from math import ceil

from django.http import HttpResponse
from rest_framework.views import APIView

from core.models import Recipe, RecipeIngredient
from foodgram.utils import (
    delete_object, get_or_create_object, get_user_shopping_cart_items
)
from shopping_list.models import ShoppingCart


def get_user_items(request):
    return get_user_shopping_cart_items(
        ShoppingCart,
        request.user,
        'Your shopping cart is empty.'
    )


class BaseRecipeAPIView(APIView):
    main_model = None
    related_model = None
    create_message = ''
    not_found_message = ''

    def post(self, request, id):
        return get_or_create_object(
            self.main_model,
            self.related_model,
            request.user,
            request,
            id,
            self.create_message
        )

    def delete(self, request, id):
        return delete_object(
            self.main_model,
            self.related_model,
            request.user,
            id,
            self.not_found_message
        )


class RecipeShoppingCartAPIView(BaseRecipeAPIView):
    main_model = Recipe
    related_model = ShoppingCart
    create_message = 'Recipe already in shopping cart.'
    not_found_message = 'Recipe not found in shopping cart.'


class DownloadShoppingCartTXTView(APIView):
    def get(self, request):
        shopping_cart_items = get_user_items(request)

        ingredients_dict = defaultdict(int)

        for item in shopping_cart_items:
            recipe = item.recipe
            for ingredient in recipe.ingredients.all():
                amount = RecipeIngredient.objects.get(
                    recipe=recipe,
                    ingredient=ingredient
                ).amount
                amount_int = int(ceil(amount))
                ingredients_dict[
                    (
                        ingredient.name,
                        ingredient.measurement_unit
                    )
                ] += amount_int

        content = ""
        for ingredient, amount in ingredients_dict.items():
            content += f"{ingredient[0]} ({ingredient[1]}) — {amount}\n"

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.txt"')
        return response


class DownloadShoppingCartJSONView(APIView):
    def get(self, request):
        shopping_cart_items = get_user_items(request)

        shopping_list = []
        for item in shopping_cart_items:
            recipe = item.recipe
            ingredients_list = [
                {
                    'name': ingredient.name,
                    'measurement_unit': ingredient.measurement_unit,
                    'amount': RecipeIngredient.objects.get(
                        recipe=recipe, ingredient=ingredient
                    ).amount
                } for ingredient in recipe.ingredients.all()
            ]
            shopping_list.append(
                {
                    'recipe_name': recipe.name,
                    'ingredients': ingredients_list
                }
            )

        response_data = json.dumps(
            shopping_list,
            ensure_ascii=False,
            indent=4
        )
        response = HttpResponse(
            response_data,
            content_type='application/json'
        )
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.json"')
        return response
