from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShowListSerializer, ShowDetailSerializer, SeasonListSerializer, EpisodeDetailSerializer
from specifications.serializers import CommentSerializer
from .models import Show, Episode
from specifications.views import CommentCreateView


class ShowListView(APIView):
    def get(self, request):
        shows = Show.objects.all()
        serializer = ShowListSerializer(shows, many=True)

        return Response(serializer.data)


class ShowDetailView(APIView):
    def get(self, request, slug):
        show = get_object_or_404(Show, slug=slug)
        comments = show.comments.filter(active=True)

        data = {
            'show': ShowDetailSerializer(show).data,
            'comments': CommentSerializer(comments, many=True).data
        }

        return Response(data)


class ShowCreateCommentView(CommentCreateView):
    def get_object(self, slug):
        return get_object_or_404(Show, slug=slug)


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