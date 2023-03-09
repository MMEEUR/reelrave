from django.contrib import admin
from .models import Movie, Picture, Trailer

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'time', 'content_rating')
    list_filter = ('release_date', 'genre', 'content_rating')
    ordering = ('-release_date',)
    search_fields = ('name', 'director')
    raw_id_fields = ('director', 'writers', 'actors')
    
@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'released')
    list_filter = ('released',)
    ordering = ('movie', 'released')
    search_fields = ('title', 'movie')
    
@admin.register(Trailer)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'released')
    list_filter = ('released',)
    ordering = ('movie', 'released')
    search_fields = ('title', 'movie')