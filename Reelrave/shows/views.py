from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ShowListSerializer, ShowDetailSerializer, EpisodeDetailSerializer
from specifications.serializers import CommentCreateSerializer, CommentSerializer
from .models import Show, Episode


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


class CreateCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        movie = get_object_or_404(Show, slug=slug)
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