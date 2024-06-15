from collections import defaultdict
from math import ceil

import pdfkit
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from core.models import Recipe, RecipeIngredient
from foodgram.constants import (
    SHOPPING_LIST_ALREADY_EXISTS, SHOPPING_LIST_NOT_FOUND,
    SHOPPING_LIST_TXT_FILENAME, SHOPPING_LIST_PDF_FILENAME
)
from foodgram.utils import (
    delete_object, get_or_create_object, get_user_shopping_cart_items
)
from shopping_list.models import ShoppingCart


def get_user_items(request):
    return get_user_shopping_cart_items(
        ShoppingCart,
        request.user
    )


class BaseRecipeAPIView(APIView):
    main_model = None
    related_model = None
    exists_message = ''
    not_found_message = ''

    def post(self, request, id):
        return get_or_create_object(
            self.main_model,
            self.related_model,
            request.user,
            request,
            id,
            self.exists_message
        )

    def delete(self, request, id):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
    exists_message = SHOPPING_LIST_ALREADY_EXISTS
    not_found_message = SHOPPING_LIST_NOT_FOUND


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
        response['Content-Disposition'] = (f'attachment; '
                                           f'filename="'
                                           f'{SHOPPING_LIST_TXT_FILENAME}"')
        return response


class DownloadShoppingCartPDFView(APIView):
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

        html_content = ("<html><head><meta charset='UTF-8'>"
                        "<title>Список покупок</title></head><body>")
        html_content += "<h1>Список покупок</h1><ul>"
        for ingredient, amount in ingredients_dict.items():
            html_content += (f"<li>{ingredient[0]} "
                             f"({ingredient[1]}) — {amount}</li>")
        html_content += "</ul></body></html>"

        # Генерация PDF из HTML
        pdf = pdfkit.from_string(html_content, False)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = (f'attachment; '
                                           f'filename="'
                                           f'{SHOPPING_LIST_PDF_FILENAME}"')
        return response
