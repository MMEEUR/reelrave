from django.shortcuts import render
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET', 'POST'])
def movie_list(request):
    data = Movie.objects.all()
    serializer_data = MovieSerializer(data, many=True)
    return Response(serializer_data.data)