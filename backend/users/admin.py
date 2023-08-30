from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Subscribe

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    empty_value_display = "-"
    list_display = ['email', 'username', 'first_name', 'last_name']
    search_fields = ["email", "username"]


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    pass
