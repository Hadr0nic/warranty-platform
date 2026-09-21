from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "role", "is_verified")
    list_filter = ("role", "is_verified")
    search_fields = ("username", "email", "phone")