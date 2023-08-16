from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model

from .serializers import CustomUserSerializer, SubscribeSerializer
from .pagination import PageLimitPagination
from users.models import Subscribe

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageLimitPagination

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        user = request.user
        subscribtions = User.objects.filter(subscribing__user=user.id)
        page = self.paginate_queryset(subscribtions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(subscribtions, many=True)
        return Response(serializer.data)
