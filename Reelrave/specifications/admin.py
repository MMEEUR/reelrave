from django.contrib import admin
from .models import Country, Genre, Photo, Video

# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_object', 'released')
    list_filter = ('released',)
    ordering = ('-released',)
    search_fields = ('title', 'content_object')
    
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_object', 'released')
    list_filter = ('released',)
    ordering = ('-released',)
    search_fields = ('title', 'content_object')