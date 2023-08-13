from rest_framework import viewsets
from rest_framework import filters

from djoser.views import UserViewSet as DjoserViewSet
from django.contrib.auth import get_user_model
from .serializers import TagSerializer, IngredientSerializer, UserSerializer
from .pagination import PagePagination
from recipes.models import Ingredient, Tag


User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PagePagination
