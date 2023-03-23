from rest_framework.serializers import ModelSerializer
from .models import Show, Season, Episode
from specifications.serializers import GenreSerializer, CountrySeralizer, PhotoSerializer, VideoSerializer, CommentSerializer
from persons.serializers import PersonSerializer

class EpisodeDetailSerializer(ModelSerializer):
    pictures = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Episode
        exclude = ('id',)
        
class EpisodeListSerializer(ModelSerializer):
    class Meta:
        model = Episode
        fields = ('number', 'time', 'baner', 'released')

class SeasonSerializer(ModelSerializer):
    episodes = EpisodeListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Season
        exclude = ('id', 'show')
        
class ShowListSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    country_of_origin = CountrySeralizer(many=True, read_only=True)
    director = PersonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Show
        fields = ('name', 'slug', 'baner', 'release_date', 'ending_date', 'content_rating', 'genre', 'director', 'description', 'country_of_origin')
        
class ShowDetailSerializer(ModelSerializer):
    seasons = SeasonSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    country_of_origin = CountrySeralizer(many=True, read_only=True)
    creators = PersonSerializer(many=True, read_only=True)
    actors = PersonSerializer(many=True, read_only=True)
    pictures = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Show
        exclude = ('id',)