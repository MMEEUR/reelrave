from rest_framework.serializers import ModelSerializer
from .models import Comment, Genre, Country, Photo, Video
from accounts.serializers import UserCommentSerializer

class CommentSerializer(ModelSerializer):
    user_profile = UserCommentSerializer(read_only=True)
    
    class Meta:
        model = Comment
        exclude = ('id', 'active', 'content_type', 'object_id')
        
class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        
class CountrySeralizer(ModelSerializer):
    class Meta:
        model = Country
        exclude = ('id',)
        
class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ('title', 'image', 'released')
        
class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'video', 'released')