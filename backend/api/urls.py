from django.urls import path, include
from rest_framework import routers

from .views import (
    CustomUserViewSet, IngredientViewSet,
    TagViewSet, RecipeViewSet
    )

router = routers.DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
