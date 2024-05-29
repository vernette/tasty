from django.contrib import admin
from django.urls import path, include

from core.views import redirect_to_recipe


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('s/<str:short_link>/', redirect_to_recipe, name='short_link'),
]
