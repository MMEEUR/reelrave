from django.contrib import admin
from .models import Person

# Register your models here.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'birthday', 'height_centimeter')
    list_filter = ('role',)
    ordering = ('name',)
    search_fields = ('name',)