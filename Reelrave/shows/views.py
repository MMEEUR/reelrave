from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShowListSerializer, ShowDetailSerializer, SeasonListSerializer, EpisodeDetailSerializer, EpisodeListSerializer
from specifications.serializers import CommentSerializer
from .models import Show, Episode
from specifications.views import CommentCreateView, CreateRatingView, WatchListView


class ShowListView(APIView):
    def get(self, request):
        shows = Show.objects.all()
        serializer = ShowListSerializer(shows, many=True)

        return Response(serializer.data)


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
    
    
class ShowCreateRatingView(CreateRatingView):
    def get_object(self, slug):
        return get_object_or_404(Show, slug=slug)
    
    
class EpisodeCreateRatingView(CreateRatingView):
    def get_object(self, episode_id):
        return get_object_or_404(Episode, id=episode_id)
    

class ShowWatchListView(WatchListView):
    def get_object(self, slug):
        return get_object_or_404(Show, slug=slug)
    
class EpisodeWatchListView(WatchListView):
    def get_object(self, episode_id):
        return get_object_or_404(Episode, id=episode_id)