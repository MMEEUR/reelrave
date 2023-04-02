from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer
from specifications.serializers import CommentSerializer
from specifications.views import CommentCreateView, CreateRatingView, WatchListView


class MovieListView(APIView):
    def get(self, request):
        shows = Movie.objects.all()
        serializer = MovieListSerializer(shows, many=True)

        return Response(serializer.data)


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
    
    
class MovieCreateRatingView(CreateRatingView):
    def get_object(self, slug):
        return get_object_or_404(Movie, slug=slug)
    
    
class MovieWatchListView(WatchListView):
    def get_object(self, slug):
        return get_object_or_404(Movie, slug=slug)