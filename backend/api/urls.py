from django.urls import path, include
from rest_framework import routers
from .views import TagViewSet, UserViewSet, IngredientViewSet


router = routers.DefaultRouter()
router.register('ingrediets', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
