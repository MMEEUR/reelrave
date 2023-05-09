from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from shows.models import Episode
from movies.models import Movie
from specifications.models import Video
from movies.serializers import FeaturedMoviesSerializer, MovieListSerializer
from specifications.serializers import VideoSerializer
from shows.serializers import LatestEpisodesSerializers
from .search import search_content
from .serializers import SearchContentserializer


class HomeView(APIView):
    
    @method_decorator(cache_page(60*60*6))
    def get(self, request):
        featured_movies = Movie.objects.filter(featured=True)[:6]
        latest_trailers = Video.objects.filter(is_trailer=True)[:6]
        latest_episodes = Episode.objects.all()[:10]
        latest_movies = Movie.objects.all()[:10]
        
        data = {
            "featured_movies": FeaturedMoviesSerializer(featured_movies, many=True).data,
            "latest_trailers": VideoSerializer(latest_trailers, many=True).data,
            "latest_episodes": LatestEpisodesSerializers(latest_episodes, many=True).data,
            "latest_movies": MovieListSerializer(latest_movies, many=True).data
        }
        
        return Response(data)
    
    
class SearchView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        
        if query:
            object_list = search_content(query)
            
            data = {
                "query": query,
                "result": SearchContentserializer(object_list, many=True).data
            }
            
            return Response(data)
            
        return Response()