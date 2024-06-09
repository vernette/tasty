import django_filters as filters

from .models import Recipe, Tag, Ingredient


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__id', lookup_expr='exact')
    is_favorited = filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.NumberFilter(method='filter_is_in_shopping_cart')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        conjoined=False
    )

    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited', 'is_in_shopping_cart', 'tags']

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and isinstance(self.request.user.id, int):
            if value == 1:
                return queryset.filter(favorites__user=self.request.user.id)
            elif value == 0:
                return queryset.exclude(favorites__user=self.request.user.id)
        return queryset.none()

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and isinstance(self.request.user.id, int):
            if value == 1:
                return queryset.filter(in_shopping_carts__user=self.request.user.id)
            elif value == 0:
                return queryset.exclude(in_shopping_carts__user=self.request.user.id)
        return queryset.none()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']