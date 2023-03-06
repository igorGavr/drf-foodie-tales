from django.contrib import admin

from apps.users.models import UserModel


@admin.register(UserModel)
class TagAdmin(admin.ModelAdmin):
    list_display = [ "email", "password", "is_active",
                    "is_staff", "created_at", "updated_at",]
