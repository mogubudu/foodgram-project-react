from django.db.models import Sum
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.exceptions import ValidationError
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .handlers import create_and_download_pdf_file

from .serializers import (
    CustomUserSerializer, SubscribeSerializer,
    IngredientSerializer, TagSerializer,
    RecipeSerializer, RecipeWriteSerializer,
    ShortRecipeSerializer
    )
from .pagination import PageLimitPagination
from recipes.models import Ingredient, IngredientAmount, Tag, Recipe, ShoppingCart, Favorite
from users.models import Subscribe


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageLimitPagination

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            subscribing__user=self.request.user
        )
        pages = self.paginate_queryset(subscriptions)
        serializer = SubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(
            User,
            id=kwargs.get('id')
        )

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={"request": request}
            )

            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(
                user=user,
                author=author
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        subscription = get_object_or_404(
            Subscribe,
            user=user,
            author=author
        )
        subscription.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            Sum('amount')
        )
        return create_and_download_pdf_file(ingredients)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, **kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=kwargs.get('pk'))

        if request.method == 'POST':
            _, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe
            )
            if not created:
                raise ValidationError(
                    {'error': 'Рецепт уже был добавлен в список покупок'}
                )
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        shopping_cart = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, **kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=kwargs.get('pk'))

        if request.method == 'POST':
            _, created = Favorite.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if not created:
                raise ValidationError(
                    {'error': 'Рецепт уже был добавлен в избранное'}
                )
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        favorite_recipe = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)