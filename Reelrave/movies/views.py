from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer
from specifications.serializers import CommentSerializer
from specifications.views import CommentCreateView, RatingView, WatchListView, GenreDetailView, CountryDetailView


class MovieListView(APIView):
    def get(self, request):
        shows = Movie.objects.all()
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(shows, request)
        serializer = MovieListSerializer(page, many=True)

        response = Response(serializer.data)
        response['Total-Count'] = paginator.page.paginator.count
        response['Page-Size'] = paginator.page_size
        response['Page'] = paginator.page.number
        
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