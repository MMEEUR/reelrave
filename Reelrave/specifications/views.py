from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Genre, Country
from .serializers import GenreSerializer, CountrySeralizer
from movies.serializers import MovieListSerializer
from shows.serializers import ShowListSerializer
# Create your views here.

class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        
        return Response(serializer.data)
    
class GenreDetailView(APIView):
    def get(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        movies = genre.genre_movies.all()
        shows = genre.genre_shows.all()
        
        serializer1 = MovieListSerializer(movies, many=True)
        serializer2 = ShowListSerializer(shows, many=True)
        
        data = {
            'genre': genre.name,
            'movies': serializer1.data,
            'shows': serializer2.data
        }
        
        return Response(data)
    
class CountryListView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySeralizer(countries, many=True)
        
        return Response(serializer.data)
    
class CountryDetailView(APIView):
    def get(self, request, slug):
        country = get_object_or_404(Country, slug=slug)
        movies = country.country_movies.all()
        shows = country.country_shows.all()
        
        serializer1 = MovieListSerializer(movies, many=True)
        serializer2 = ShowListSerializer(shows, many=True)
        
        data = {
            'country': country.name,
            'movies': serializer1.data,
            'shows': serializer2.data
        }
        
        return Response(data)