from rest_framework.serializers import ModelSerializer, FloatField, IntegerField
from .models import Movie
from persons.serializers import PersonSerializer
from specifications.serializers import GenreSerializer, CountrySeralizer, PhotoSerializer, VideoSerializer


class TopMoviesSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name', 'baner', 'get_absolute_url',
                  'release_date', 'total_ratings', 'average_rating')
        
        
class FeaturedMoviesSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id' 'name', 'baner', 'get_absolute_url',
                  'release_date', 'average_rating')


class MovieDetailSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    country_of_origin = CountrySeralizer(many=True, read_only=True)
    director = PersonSerializer(many=True, read_only=True)
    writers = PersonSerializer(many=True, read_only=True)
    actors = PersonSerializer(many=True, read_only=True)
    pictures = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    average_rating = FloatField()
    total_ratings = IntegerField()

    class Meta:
        model = Movie
        fields = "__all__"


class MovieListSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    country_of_origin = CountrySeralizer(many=True, read_only=True)
    director = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'get_absolute_url', 'average_rating', 'baner', 'release_date',
                  'time', 'content_rating', 'genre', 'director', 'description', 'country_of_origin')