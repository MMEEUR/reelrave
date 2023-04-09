from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q, Count
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    ShowListSerializer, ShowDetailSerializer,
    SeasonListSerializer, EpisodeDetailSerializer,
    EpisodeListSerializer, TopShowsSerializer
)
from specifications.serializers import CommentSerializer
from .models import Show, Episode
from specifications.models import Genre
from specifications.views import CommentCreateView, RatingView, WatchListView, GenreDetailView, CountryDetailView


class TopShowsView(APIView):
    def get(self, request, genre=None):
        if genre:
            genre_obj = get_object_or_404(Genre, slug=genre)
        
        cache_key = f"top_shows:{genre}"
        cached_result = cache.get(cache_key)
        
        if cached_result is not None:
            return Response(cached_result)
        
        minimum_ratings = 1
        minimum_episodes = 1
        
        if genre:
            top_movies = Show.objects.filter(genre=genre_obj)\
                        .annotate(num_ratings=Count('ratings'))\
                        .filter(num_ratings__gte=minimum_ratings)\
                        .annotate(num_episodes=Count('seasons__episodes'))\
                        .filter(num_episodes__gte=minimum_episodes)\
                        .annotate(avg_rating=Avg('ratings__rating', filter=~Q(ratings__rating=0)))\
                        .order_by('-avg_rating')[:250]

        else:
            top_movies = Show.objects.annotate(num_ratings=Count('ratings'))\
                        .filter(num_ratings__gte=minimum_ratings)\
                        .annotate(num_episodes=Count('seasons__episodes'))\
                        .filter(num_episodes__gte=minimum_episodes)\
                        .annotate(avg_rating=Avg('ratings__rating', filter=~Q(ratings__rating=0)))\
                        .order_by('-avg_rating')[:250]
        
        serializer = TopShowsSerializer(top_movies, many=True)
        
        if serializer:
            cache.set(cache_key, serializer.data, 86400) # cache for 24 hours
        
        return Response(serializer.data)


class ShowListView(APIView):
    def get(self, request):
        shows = Show.objects.all()
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(shows, request)
        serializer = ShowListSerializer(page, many=True)

        response = Response(serializer.data)
        response['Total-Count'] = paginator.page.paginator.count
        response['Page-Size'] = paginator.page_size
        response['Page'] = paginator.page.number
        
        return response


class ShowDetailView(APIView):
    def get(self, request, slug):
        show = get_object_or_404(Show, slug=slug)
        comments = show.comments.filter(active=True)
        top_rated_episodes = show.get_top_rated_episodes()
        most_recent_episode = show.get_most_recent_episode()

        data = {
            "show": ShowDetailSerializer(show).data,
            "comments": CommentSerializer(comments, many=True).data,
            "top_rated_episodes": EpisodeListSerializer(top_rated_episodes, many=True).data,
            "most_recent_episode": EpisodeListSerializer(most_recent_episode).data
        }

        return Response(data)


class EpisodeListView(APIView):
    def get(self, request, slug):
        show = get_object_or_404(Show, slug=slug)
        seasons = show.seasons.all()
        serializer = SeasonListSerializer(seasons, many=True)

        data = {
            "show": f"{show.name}",
            "seasons": serializer.data
        }

        return Response(data)


class EpisodeDetailView(APIView):
    def get(self, request, slug, episode_id):
        episode = get_object_or_404(Episode, id=episode_id)
        serializer = EpisodeDetailSerializer(episode)

        data = {
            "show": f"{episode.season.show.name}",
            "number": f"S{episode.season.number}.E{episode.number}",
            "episode": serializer.data
        }

        return Response(data)


class ShowCreateCommentView(CommentCreateView):
    def get_object(self, slug):
        return get_object_or_404(Show, slug=slug)
    
    
class EpisodeCreateCommentView(CommentCreateView):
    def get_object(self, episode_id):
        return get_object_or_404(Episode, id=episode_id)
    
    
class ShowRatingView(RatingView):
    def get_object(self, slug):
        return get_object_or_404(Show, slug=slug)
    
    
class EpisodeRatingView(RatingView):
    def get_object(self, episode_id):
        return get_object_or_404(Episode, id=episode_id)
    

class ShowWatchListView(WatchListView):
    def get_object(self, slug):
        return get_object_or_404(Show, slug=slug)
    
    
class EpisodeWatchListView(WatchListView):
    def get_object(self, episode_id):
        return get_object_or_404(Episode, id=episode_id)
    

class ShowGenreView(GenreDetailView):
    model = "shows"
    serializer_class = ShowListSerializer


class ShowCountryView(CountryDetailView):
    model = "shows"
    serializer_class = ShowListSerializer