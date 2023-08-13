from rest_framework import serializers
from djoser.serializers import (
    UserCreateSerializer as DjoserCreateSerializer,
    UserSerializer as DjoserSerializer
)
from django.contrib.auth import get_user_model
from recipes.models import Tag
from users.models import Subscribe

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserCreateSerializer(DjoserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class UserSerializer(DjoserSerializer):
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribe')

    def get_is_subscribe(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscribe.objects.filter(user=user, author=obj).exists()
        return False
