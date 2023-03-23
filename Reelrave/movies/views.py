from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer
from specifications.serializers import CommentCreateSerializer, CommentSerializer

# Create your views here.
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
    
    def post(self, request, slug):
        if not request.user.is_authenticated:
            return Response({"error": 'You must login before you post a comment'}, status=HTTP_401_UNAUTHORIZED)
        
        movie = get_object_or_404(Movie, slug=slug)
        content_type = ContentType.objects.get_for_model(movie)
        
        # update data with content_type and object_id
        data = request.data
        data['user'] = request.user.id
        data['content_type'] = content_type.id
        data['object_id'] = movie.id
        
        serializer = CommentCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=HTTP_201_CREATED)