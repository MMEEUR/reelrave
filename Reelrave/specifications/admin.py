from django.contrib import admin
from .models import Country, Genre, Photo, Video, Comment

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
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'created', 'active')
    list_filter = ('active', 'created')
    ordering = ('active', '-created')
    search_fields = ('user', 'body', 'content_object')
    
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