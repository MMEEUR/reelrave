from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Show, Season, Episode
from specifications.models import Photo, Video

#Register your models here.
class PhotoInline(GenericTabularInline):
    model = Photo
    
class VideoInline(GenericTabularInline):
    model = Video
    
@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_genres', 'release_date', 'ending_date', 'content_rating', 'season_count', 'episode_count', 'comments_count')
    list_filter = ('content_rating', 'release_date', 'genre')
    search_fields = ('name', 'director')
    ordering = ('-release_date',)
    raw_id_fields = ('creators', 'actors', 'country_of_origin')
    inlines = [PhotoInline, VideoInline]

    @admin.display(description='Comments')
    def comments_count(self, obj):
        return obj.comments.count()
    
    @admin.display(description='Genres')
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('show', 'number', 'episode_count')
    search_fields = ('show',)
    ordering = ('show', '-number')
    raw_id_fields = ('show',)
    
    def episode_count(self, obj):
        return obj.episodes.count()
    episode_count.short_description = 'Episodes'

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'number', 'name', 'time', 'release_date')
    list_filter = ('release_date',)
    search_fields = ('season', 'name')
    ordering = ('-release_date', '-season')
    raw_id_fields = ('season',)
    inlines = [PhotoInline, VideoInline]