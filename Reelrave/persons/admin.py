from django.contrib import admin
from .models import Person, Role


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_roles', 'birthday', 'height_centimeter')
    list_filter = ('roles',)
    ordering = ('name',)
    search_fields = ('name',)

    @admin.display(description='Roles')
    def display_roles(self, obj):
        return ", ".join([role.role for role in obj.roles.all()])


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role',)
    ordering = ('role',)
    search_fields = ('role',)
    raw_id_fields = ('persons',)