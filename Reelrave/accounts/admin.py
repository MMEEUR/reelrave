from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, PasswordReset, EmailConfirm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ["username", "email", "is_staff", "comments_count"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("bio", "date_of_birth", "photo")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("bio", "date_of_birth", "photo")}),)
    
    
@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user",)
    
    
@admin.register(EmailConfirm)
class EmailConfirmAdmin(admin.ModelAdmin):
    list_display = ("email", "code", "created_at")
    search_fields = ("email",)