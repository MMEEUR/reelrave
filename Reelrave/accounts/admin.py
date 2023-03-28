from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProflieAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'comments_count')
    ordering = ('user',)
    search_fields = ('user',)