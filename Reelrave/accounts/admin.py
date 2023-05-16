from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ["username", "email", "is_staff", "comments_count"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("bio", "date_of_birth", "photo")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("bio", "date_of_birth", "photo")}),)