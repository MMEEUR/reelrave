from rest_framework.serializers import ModelSerializer, FloatField, IntegerField
from .models import Show, Season, Episode
from specifications.serializers import GenreSerializer, CountrySeralizer, PhotoSerializer, VideoSerializer, CommentSerializer
from persons.serializers import PersonSerializer


class TopShowsSerializer(ModelSerializer):
    class Meta:
        model = Show
        fields = ('id', 'name', 'baner', 'get_absolute_url',
                  'release_date', 'total_ratings', 'average_rating')


class EpisodeListSerializer(ModelSerializer):
    class Meta:
        model = Episode
        fields = ('number', 'name', 'id', 'get_absolute_url',
                  'average_rating', 'baner', 'release_date')


class SeasonListSerializer(ModelSerializer):
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
        fields = ('id', 'name', 'get_absolute_url', 'average_rating', 'baner', 'release_date', 'ending_date',
                  'content_rating', 'genre', 'director', 'description', 'country_of_origin')


class ShowDetailSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    country_of_origin = CountrySeralizer(many=True, read_only=True)
    creators = PersonSerializer(many=True, read_only=True)
    actors = PersonSerializer(many=True, read_only=True)
    pictures = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    average_rating = FloatField()
    total_ratings = IntegerField()

    class Meta:
        model = Show
        fields = "__all__"


class EpisodeDetailSerializer(ModelSerializer):
    pictures = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    director = PersonSerializer(many=True, read_only=True)
    writers = PersonSerializer(many=True, read_only=True)
    actors = PersonSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    average_rating = FloatField()
    total_ratings = IntegerField()
    
    class Meta:
        model = Episode
        fields = "__all__"
        
        
class LatestEpisodesSerializers(ModelSerializer):
    class Meta:
        model = Episode
        fields = ('id', 'name', 'title', 'baner', 'get_absolute_url')