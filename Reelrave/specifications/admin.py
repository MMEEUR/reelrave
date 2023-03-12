from django.contrib import admin
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from .models import Country, Genre, Photo, Video

class MediaForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(model__in=['show', 'movie', 'episode'])
    )
    content_object_id = forms.IntegerField(widget=ForeignKeyRawIdWidget(ContentType.objects.all(), admin_site=admin.site))

    class Meta:
        abstract = True

class PhotoForm(MediaForm):
    class Meta:
        model = Photo
        fields = ['title', 'content_type', 'content_object_id', 'image']

class VideoForm(MediaForm):
    class Meta:
        model = Video
        fields = ['title', 'content_type', 'content_object_id', 'video']

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    form = PhotoForm
    list_display = ('title', 'content_object', 'released')
    list_filter = ('released',)
    ordering = ('-released',)
    search_fields = ('title', 'content_object')
    
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoForm 
    list_display = ('title', 'content_object', 'released')
    list_filter = ('released',)
    ordering = ('-released',)
    search_fields = ('title', 'content_object')
    
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