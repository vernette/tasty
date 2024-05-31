from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.models import Recipe
from favorites.models import Favorite
from core.serializers import RecipeSerializer


class RecipeFavoriteAPIView(APIView):
    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        if created:
            response_data = {
                "id": recipe.id,
                "name": recipe.name,
                "image": request.build_absolute_uri(recipe.image.url),
                "cooking_time": recipe.cooking_time
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({'errors': 'Рецепт уже в избранном.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe).first()
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепта нет в избранном.'},
                            status=status.HTTP_400_BAD_REQUEST)