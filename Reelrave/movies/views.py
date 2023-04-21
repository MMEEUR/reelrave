from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q, Count
from django.core.cache import cache
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Movie
from specifications.models import Genre
from .serializers import MovieListSerializer, MovieDetailSerializer, TopMoviesSerializer
from specifications.serializers import CommentSerializer, GenreSerializer
from specifications.views import CommentCreateView, RatingView, WatchListView, GenreDetailView, CountryDetailView


class TopMoviesView(APIView):
    def get(self, request, genre=None):
        movie_genres = Genre.objects.filter(genre_movies__isnull=False).distinct()
        
        if genre:
            genre_obj = get_object_or_404(Genre, slug=genre)
        
        cache_key = f"top_movies:{genre}"
        cached_result = cache.get(cache_key)
        
        if cached_result is not None:
            data = {
                "top_movies": cached_result,
                "movie_genres": GenreSerializer(movie_genres, many=True).data
            }
            
            return Response(data)
        
        minimum_ratings = settings.MOVIE_MINIMUM_RATINGS
        
        if genre:
            top_movies = Movie.objects.filter(genre=genre_obj,)\
                        .annotate(num_ratings=Count('ratings'))\
                        .filter(num_ratings__gte=minimum_ratings)\
                        .annotate(avg_rating=Avg('ratings__rating', filter=~Q(ratings__rating=0)))\
                        .order_by('-avg_rating')[:250]

        else:
            top_movies = Movie.objects.annotate(num_ratings=Count('ratings'))\
                        .filter(num_ratings__gte=minimum_ratings)\
                        .annotate(avg_rating=Avg('ratings__rating', filter=~Q(ratings__rating=0)))\
                        .order_by('-avg_rating')[:250]
        
        movie_serializer = TopMoviesSerializer(top_movies, many=True)
        
        if top_movies:
            cache.set(cache_key, movie_serializer.data, 86400) # cache for 24 hours
            
        data = {
            "top_movies": movie_serializer.data,
            "movie_genres": GenreSerializer(movie_genres, many=True).data
        }
        
        return Response(data)


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(movies, request)
        serializer = MovieListSerializer(page, many=True)

        response = Response(serializer.data)
        response['X-Total-Count'] = paginator.page.paginator.count
        response['X-Page-Size'] = paginator.page_size
        response['X-Page'] = paginator.page.number

        return response


class MovieDetailView(APIView):
    def get(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        comments = movie.comments.filter(active=True)

        data = {
            'movie': MovieDetailSerializer(movie).data,
            'comments': CommentSerializer(comments, many=True).data
        }

        return Response(data)


class MovieCreateCommentView(CommentCreateView):
    def get_object(self, slug):
        return get_object_or_404(Movie, slug=slug)


class MovieRatingView(RatingView):
    def get_object(self, slug):
        return get_object_or_404(Movie, slug=slug)


class MovieWatchListView(WatchListView):
    def get_object(self, slug):
        return get_object_or_404(Movie, slug=slug)


class MovieGenreView(GenreDetailView):
    model = "movies"
    serializer_class = MovieListSerializer


class MovieCountryView(CountryDetailView):
    model = "movies"
    serializer_class = MovieListSerializer