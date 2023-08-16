from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

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
        subscriptions = User.objects.filter(subscribing__user=self.request.user)
        pages = self.paginate_queryset(subscriptions)
        serializer = SubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)
