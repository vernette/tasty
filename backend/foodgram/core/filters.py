import django_filters as filters

from .models import Recipe, Tag, Ingredient


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__id', lookup_expr='exact')
    is_favorited = filters.NumberFilter(method='filter_by_user_related_field')
    is_in_shopping_cart = filters.NumberFilter(method='filter_by_user_related_field')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        conjoined=False
    )

    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited', 'is_in_shopping_cart', 'tags']

    def filter_by_user_related_field(self, queryset, name, value):
        field_mapping = {
            'is_favorited': 'favorites__user',
            'is_in_shopping_cart': 'in_shopping_cart__user'
        }
        filter_kwargs = {field_mapping.get(name): self.request.user.id}
        return (queryset.filter(**filter_kwargs) if value == 1
                else queryset.exclude(**filter_kwargs))


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']
