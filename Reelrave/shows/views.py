from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from .serializers import ShowListSerializer, ShowDetailSerializer
from specifications.serializers import CommentCreateSerializer, CommentSerializer
from .models import Show

# Create your views here.
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
    
    def post(self, request, slug):
        if not request.user.is_authenticated or not request.user.profile:
            return Response(status=HTTP_401_UNAUTHORIZED)
        
        show = get_object_or_404(Show, slug=slug)
        content_type = ContentType.objects.get_for_model(show)
        
        # update data with content_type and object_id
        data = request.data
        data['user_profile'] = request.user.profile.id
        data['content_type'] = content_type.id
        data['object_id'] = show.id
        
        serializer = CommentCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=HTTP_201_CREATED)