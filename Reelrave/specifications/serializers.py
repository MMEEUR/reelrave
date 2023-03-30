from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Comment, CommentLikeDisLike, Genre, Country, Photo, Video, Rating
from accounts.serializers import UserCommentSerializer


class RatingCreateSerializer(ModelSerializer):
    class Meta:
        model = Rating
        exclude = ('id',)


class RatingUpdateSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating',)


class CommentLikeDisLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLikeDisLike
        fields = ('like_or_dislike',)


class CommentSerializer(ModelSerializer):
    user = UserCommentSerializer(read_only=True)
    likes_count = IntegerField()
    dislikes_count = IntegerField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'body', 'likes_count',
                  'dislikes_count', 'created', 'updated')


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('id', 'active',)


class CommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body',)


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