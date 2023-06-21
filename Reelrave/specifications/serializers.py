from rest_framework.serializers import (
    SlugField, ImageField,
    DateField, CharField, URLField,
    DurationField, FloatField, IntegerField,
    ModelSerializer, Serializer
)
from .models import Comment, CommentLikeDisLike, Genre, Country, Photo, Video, Rating, WatchList
from accounts.serializers import UserCommentSerializer


class OriginContentSerializer(Serializer):
    name = CharField()
    title = CharField(required=False)
    get_absolute_url = URLField()
    
    
class PhotoListSerializer(ModelSerializer):
    content_object = OriginContentSerializer(read_only=True)
    
    class Meta:
        model = Photo
        fields = ('title', 'image', 'released', 'content_object')


class VideoListSerializer(ModelSerializer):
    content_object = OriginContentSerializer(read_only=True)
    
    class Meta:
        model = Video
        fields = ('title', 'video', 'released', 'is_trailer', 'content_object')
        

class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ('title', 'image', 'released')


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'video', 'released', 'is_trailer')
        
        
class CountrySeralizer(ModelSerializer):
    class Meta:
        model = Country
        exclude = ('id',)


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class GenreCountryListSerializer(Serializer):
    name = CharField()
    slug = SlugField()
    flag = ImageField(required=False)
    movies_count = IntegerField(required=False)
    shows_count = IntegerField(required=False)
    
    def __init__(self, *args, **kwargs):
        include_movies_count = kwargs.pop('include_movies_count', True)
        
        super().__init__(*args, **kwargs)
        
        if include_movies_count and 'shows_count' in self.fields:
            self.fields.pop('shows_count')
        
        elif not include_movies_count and 'movies_count' in self.fields:
            self.fields.pop('movies_count')


class ContentSerializer(Serializer):
    name = CharField()
    title = CharField(required=False)
    baner = ImageField()
    get_absolute_url = URLField()
    release_date = DateField()
    ending_date = DateField(required=False)
    time = DurationField(required=False)
    season_count = IntegerField(required=False)
    episode_count = IntegerField(required=False)
    content_rating = CharField()
    genre = GenreSerializer(many=True, read_only=True)
    average_rating = FloatField()
    description = CharField()


class ActivitySerializer(Serializer):
    content_type = CharField()
    object_id = IntegerField()
    rating = FloatField(required=False)


class WatchListSerializer(ModelSerializer):
    content_object = ContentSerializer(read_only=True)
    
    class Meta:
        model = WatchList
        fields = ('content_object', 'created')


class WatchListAddSerializer(ModelSerializer):
    class Meta:
        model = WatchList
        exclude = ('id', 'created')


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
        exclude = ('id',)
        
        
class CommentLikeDisLikeUpdateSerializer(ModelSerializer):
    class Meta:
        model = CommentLikeDisLike
        fields = ('like_or_dislike',)


class CommentSerializer(ModelSerializer):
    user = UserCommentSerializer(read_only=True)

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