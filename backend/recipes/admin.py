from django.contrib import admin
from .models import Recipe, Tag

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
