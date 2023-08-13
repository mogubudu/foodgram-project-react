from rest_framework import viewsets

from djoser.views import UserViewSet as DjoserViewSet
from django.contrib.auth import get_user_model
from .serializers import TagSerializer, UserSerializer
from .pagination import PagePagination
from recipes.models import Tag


User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PagePagination