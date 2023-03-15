from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie
from specifications.models import Comment
from .serializers import MovieSerializer
from specifications.serializers import CommentSerializer

# Create your views here.
@api_view(['GET'])
def movie_list(request):
    data = Movie.objects.all()
    serializer = MovieSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

class MovieCommentView(APIView):
    def get(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        content_type = ContentType.objects.get_for_model(movie)
        movie_comments = Comment.objects.filter(content_type=content_type, object_id=movie.id, active=True)
        serializer = CommentSerializer(movie_comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, slug):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)