from django.contrib import admin
from .models import Movie

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'time', 'content_rating')
    list_filter = ('release_date', 'genre', 'content_rating')
    ordering = ('-release_date',)
    search_fields = ('name', 'director')
    raw_id_fields = ('director', 'writers', 'actors', 'country_of_origin')