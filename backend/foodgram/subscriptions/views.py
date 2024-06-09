from rest_framework import status, views, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import SubscriptionSerializer
from .models import Subscription


User = get_user_model()


class SubscribeView(views.APIView):
    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user == author:
            return Response({'error': 'You cannot subscribe to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscription.objects.filter(user=request.user, author=author)
        if subscription.exists():
            return Response({'error': 'Subscription already exists'}, status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.get_or_create(user=request.user, author=author)
        serializer = SubscriptionSerializer(author, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        subscription = Subscription.objects.filter(user=request.user, author=author)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Subscription does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        subscriptions = Subscription.objects.filter(user=user).select_related('author')
        return User.objects.filter(id__in=subscriptions.values('author_id'))
