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
    list_filter = ('content_rating', 'release_date')
    search_fields = ('name', 'director')
    ordering = ('-release_date',)
    raw_id_fields = ('creators', 'actors', 'country_of_origin')
    inlines = [PhotoInline, VideoInline]
    
    def season_count(self, obj):
        return obj.seasons.count()
    season_count.short_description = 'Seasons'
    
    def episode_count(self, obj):
        episode_count = 0
        for season in obj.seasons.all():
            episode_count += season.episodes.count()
        return episode_count
    episode_count.short_description = 'Episodes'

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'
    
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    display_genres.short_description = 'Genres'
    
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('show', 'number', 'episode_count')
    search_fields = ('show',)
    ordering = ('show', '-number')
    
    def episode_count(self, obj):
        return obj.episodes.count()
    episode_count.short_description = 'Episodes'

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'number', 'title', 'time', 'released')
    list_filter = ('released',)
    search_fields = ('season', 'title')
    ordering = ('-released', '-season')
    inlines = [PhotoInline, VideoInline]