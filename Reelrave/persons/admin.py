from django.contrib import admin
from .models import Person, Role

# Register your models here.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_roles', 'birthday', 'height_centimeter')
    list_filter = ('roles',)
    ordering = ('name',)
    search_fields = ('name',)
    
    def display_roles(self, obj):
        return ", ".join([role.role for role in obj.roles.all()])
    display_roles.short_description = 'Roles'
    
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role',)
    ordering = ('role',)
    search_fields = ('role',)
    raw_id_fields = ('person',)