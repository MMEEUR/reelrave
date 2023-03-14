from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Movie
from specifications.models import Photo, Video

#Register your models here.
class PhotoInline(GenericTabularInline):
    model = Photo
    
class VideoInline(GenericTabularInline):
    model = Video

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_genres', 'release_date', 'time', 'content_rating', 'comments_count')
    list_filter = ('release_date', 'genre', 'content_rating')
    ordering = ('-release_date',)
    search_fields = ('name', 'director')
    raw_id_fields = ('director', 'writers', 'actors', 'country_of_origin')
    inlines = [PhotoInline, VideoInline]
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'
    
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    display_genres.short_description = 'Genres'