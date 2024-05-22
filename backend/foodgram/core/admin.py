from django.contrib import admin

from core.models import Recipe, Ingredient, Tag


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
