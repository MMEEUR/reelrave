from django.contrib import admin
from .models import Show, Season, Episode

# Register your models here.
@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'ending_date', 'content_rating', 'season_count', 'episode_count')
    list_filter = ('content_rating', 'release_date')
    search_fields = ('name', 'director')
    ordering = ('-release_date',)
    raw_id_fields = ('director', 'writers', 'actors', 'country_of_origin')
    
    def season_count(self, obj):
        return obj.seasons.count()
    season_count.short_description = 'Seasons'
    
    def episode_count(self, obj):
        episode_count = 0
        for season in obj.seasons.all():
            episode_count += season.episodes.count()
        return episode_count
    episode_count.short_description = 'Episodes'

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