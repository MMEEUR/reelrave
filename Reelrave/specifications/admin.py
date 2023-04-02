from django.contrib import admin
from .models import Country, Genre, Photo, Video, Comment, CommentLikeDisLike, Rating, WatchList


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
    list_display = ('user', 'content_object', 'likes_count', 'dislikes_count', 'created', 'active')
    list_filter = ('active', 'created')
    ordering = ('active', '-created')
    search_fields = ('user', 'body', 'content_object')
    

@admin.register(CommentLikeDisLike)
class CommentLikeDisLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'opinion', 'updated')
    list_filter = ('updated',)
    ordering = ('-updated',)
    search_fields = ('user', 'comment')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'rating', 'created', 'updated')
    list_filter = ('updated',)
    ordering = ('-updated',)
    search_fields = ('user', 'content_object')


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'created')
    list_filter = ('created',)
    ordering = ('-created',)
    search_fields = ('user', 'content_object')


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