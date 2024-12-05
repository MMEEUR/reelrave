from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, PasswordReset, EmailConfirm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("username", "email", "is_staff", "comments_count")
    list_filter = ("is_staff",)
    search_fields = ("username", "email")
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email", "bio", "date_of_birth", "photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "bio", "date_of_birth", "photo"),
        }),
    )
    
    
@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ("user", "expires")
    search_fields = ("user",)
    
    
@admin.register(EmailConfirm)
class EmailConfirmAdmin(admin.ModelAdmin):
    list_display = ("email", "code", "expires")
    search_fields = ("email",)