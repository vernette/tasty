from django.urls import path

from .views import SubscribeView, SubscriptionListView


urlpatterns = [
    path(
        'users/<int:id>/subscribe/',
        SubscribeView.as_view(),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        SubscriptionListView.as_view(),
        name='user-subscriptions'
    ),
]
