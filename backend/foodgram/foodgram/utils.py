from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def get_or_create_object(main_model, related_model, user, request, id, message):
    obj = get_object_or_404(main_model, id=id)
    instance, created = related_model.objects.get_or_create(
        user=user,
        recipe=obj
    )
    if created:
        response_data = {
            'id': obj.id,
            'name': obj.name,
            'image': request.build_absolute_uri(obj.image.url),
            'cooking_time': obj.cooking_time
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(
        {'message': message},
        status=status.HTTP_400_BAD_REQUEST
    )


def delete_object(main_model, related_model, user, id, not_found_message):
    obj = get_object_or_404(main_model, id=id)
    instance = related_model.objects.filter(user=user, recipe=obj).first()
    if instance:
        instance.delete()
        return Response(
            {'message': 'Removed successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
    return Response({
        'errors': not_found_message},
        status=status.HTTP_400_BAD_REQUEST
    )


def get_user_shopping_cart_items(model, user, empty_message):
    items = model.objects.filter(user=user).select_related('recipe')
    if not items.exists():
        return Response(
            {'errors': empty_message},
            status=status.HTTP_400_BAD_REQUEST
        )
    return items
