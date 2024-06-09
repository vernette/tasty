from django.urls import include, path


urlpatterns = [
    path('', include('core.urls')),
    path('', include('users.urls')),
    path('', include('subscriptions.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
