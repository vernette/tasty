from django.urls import path
from .views import AvatarView


urlpatterns = [
    path('users/me/avatar/', AvatarView.as_view(), name='avatar'),
]
