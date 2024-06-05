import django_filters as filters

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.NumberFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, name, value):
        if value == 1:
            return queryset.filter(favorites__user=self.request.user)
        elif value == 0:
            return queryset.exclude(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value == 1:
            return queryset.filter(in_shopping_carts__user=self.request.user)
        elif value == 0:
            return queryset.exclude(in_shopping_carts__user=self.request.user)
        return queryset
