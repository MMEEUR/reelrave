from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer
from specifications.serializers import CommentSerializer

# Create your views here.
class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer

class MovieDetailView(APIView):
    def get(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        serializer = MovieDetailSerializer(movie)
        
        return Response(serializer.data)
    
    def post(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        content_type = ContentType.objects.get_for_model(movie)
        
        # update data with content_type and object_id
        data = request.data
        data['user_profile'] = request.user.profile.id
        data['content_type'] = content_type.id
        data['object_id'] = movie.id
        
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=HTTP_201_CREATED)