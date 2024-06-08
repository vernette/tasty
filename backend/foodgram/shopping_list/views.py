import json
from collections import defaultdict
from math import ceil

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from core.models import Recipe, RecipeIngredient
from .models import ShoppingCart


class RecipeShoppingCartAPIView(APIView):
    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user, recipe=recipe)
        if created:
            response_data = {
                "id": recipe.id,
                "name": recipe.name,
                "image": request.build_absolute_uri(recipe.image.url),
                "cooking_time": recipe.cooking_time
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Recipe already in shopping cart.'}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        shopping_cart = ShoppingCart.objects.filter(user=request.user, recipe=recipe).first()
        if shopping_cart:
            shopping_cart.delete()
            return Response({'message': 'Recipe removed from shopping cart.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Recipe not found in shopping cart.'}, status=status.HTTP_400_BAD_REQUEST)


class DownloadShoppingCartTXTView(APIView):
    def get(self, request):
        shopping_cart_items = ShoppingCart.objects.filter(user=request.user).select_related('recipe')

        if not shopping_cart_items.exists():
            return Response({'errors': 'Your shopping cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        ingredients_dict = defaultdict(int)

        for item in shopping_cart_items:
            recipe = item.recipe
            for ingredient in recipe.ingredients.all():
                amount = RecipeIngredient.objects.get(recipe=recipe, ingredient=ingredient).amount
                amount_int = int(ceil(amount))
                ingredients_dict[(ingredient.name, ingredient.measurement_unit)] += amount_int

        content = ""
        for ingredient, amount in ingredients_dict.items():
            content += f"{ingredient[0]} ({ingredient[1]}) — {amount}\n"

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response


class DownloadShoppingCartJSONView(APIView):
    def get(self, request):
        shopping_cart_items = ShoppingCart.objects.filter(user=request.user).select_related('recipe')

        if not shopping_cart_items.exists():
            return Response({'errors': 'Your shopping cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        shopping_list = []
        for item in shopping_cart_items:
            recipe = item.recipe
            ingredients_list = [{'name': ingredient.name, 'measurement_unit': ingredient.measurement_unit, 'amount': RecipeIngredient.objects.get(recipe=recipe, ingredient=ingredient).amount} for ingredient in recipe.ingredients.all()]
            shopping_list.append({'recipe_name': recipe.name, 'ingredients': ingredients_list})

        response_data = json.dumps(shopping_list, ensure_ascii=False, indent=4)
        response = HttpResponse(response_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.json"'
        return response
