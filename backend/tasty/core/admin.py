from django.contrib import admin

from core.models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('name', 'author_name', 'favorites_count')
    search_fields = ('name', 'author__username')
    list_filter = ('tags',)

    def author_name(self, obj):
        return obj.author.username

    def favorites_count(self, obj):
        return obj.favorites.count()

    author_name.short_description = 'Автор'
    favorites_count.short_description = 'Число добавлений в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


admin.site.register(Recipe, RecipeAdmin)
