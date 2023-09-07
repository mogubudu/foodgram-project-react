from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscribe

from .filters import IngredientFilter, RecipeFilter
from .handlers import create_and_download_pdf_file
from .pagination import PageLimitPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeWriteSerializer,
                          ShortRecipeSerializer, SubscribeSerializer,
                          TagSerializer)

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
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request})
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
                context={"request": request}
            )

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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    http_method_names = ['get']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
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

    def create_recipe(self, user, model, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        _, created = model.objects.get_or_create(
            user=user, recipe=recipe
        )
        if not created:
            raise ValidationError(
                {'error': 'Рецепт уже был добавлен'}
            )
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, user, model, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart = model.objects.filter(
            user=user,
            recipe=recipe
        )
        if shopping_cart.exists():
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, **kwargs):
        if request.method == 'POST':
            return self.create_recipe(request.user,
                                      ShoppingCart,
                                      kwargs.get('pk'))
        return self.delete_recipe(request.user, ShoppingCart, kwargs.get('pk'))

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, **kwargs):
        if request.method == 'POST':
            return self.create_recipe(request.user, Favorite, kwargs.get('pk'))
        return self.delete_recipe(request.user, Favorite, kwargs.get('pk'))
