from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from rest_framework.pagination import PageNumberPagination
from .models import Genre, Country, Comment, CommentLikeDisLike, Rating, WatchList, Photo, Video
from .serializers import (
    RatingCreateSerializer, RatingUpdateSerializer,
    CommentUpdateSerializer, CommentCreateSerializer,
    CommentLikeDisLikeSerializer, CommentLikeDisLikeUpdateSerializer,
    WatchListAddSerializer, GenreCountryListSerializer,
    VideoListSerializer, PhotoListSerializer
)


class PhotoListView(APIView):
    def get(self, request):
        photos = Photo.objects.all()
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(photos, request)
        serializer = PhotoListSerializer(page, many=True)
        
        response = Response(serializer.data)
        response['X-Total-Count'] = paginator.page.paginator.count
        response['X-Page-Size'] = paginator.page_size
        response['X-Page'] = paginator.page.number
        
        return response
    
    
class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(videos, request)
        serializer = VideoListSerializer(page, many=True)
        
        response = Response(serializer.data)
        response['X-Total-Count'] = paginator.page.paginator.count
        response['X-Page-Size'] = paginator.page_size
        response['X-Page'] = paginator.page.number
        
        return response


class WatchListView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        raise NotImplementedError(
            'Subclasses of CommentView must define get_object method')
    
    def post(self, request, slug, episode_id=None):
        if episode_id:
            obj = self.get_object(episode_id)
            content_type = ContentType.objects.get_for_model(obj)

        else:
            obj = self.get_object(slug)
            content_type = ContentType.objects.get_for_model(obj)

        data = {}
        data['user'] = request.user.id
        data['content_type'] = content_type.id
        data['object_id'] = obj.id

        serializer = WatchListAddSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)
    
    def delete(self, request, slug, episode_id=None):
        if episode_id:
            obj = self.get_object(episode_id)
            content_type = ContentType.objects.get_for_model(obj)

        else:
            obj = self.get_object(slug)
            content_type = ContentType.objects.get_for_model(obj)

        watchlist = get_object_or_404(WatchList, user=request.user, content_type=content_type.id, object_id=obj.id)
        watchlist.delete()
        
        return Response(status=HTTP_204_NO_CONTENT)


class CommentLikeDisLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, comment_id):
        data = request.data
        
        data['comment'] = comment_id
        data['user'] = request.user.id

        serializer = CommentLikeDisLikeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=HTTP_201_CREATED)
        
    def patch(self, request, comment_id):
        comment_opinion = get_object_or_404(CommentLikeDisLike, comment=comment_id, user=request.user)
        
        serializer = CommentLikeDisLikeUpdateSerializer(comment_opinion, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def delete(self, request, comment_id):
        comment_opinion = get_object_or_404(CommentLikeDisLike, comment=comment_id, user=request.user)
        comment_opinion.delete()
        
        return Response(status=HTTP_204_NO_CONTENT)


class RatingView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        raise NotImplementedError(
            'Subclasses of CommentView must define get_object method')

    def post(self, request, slug, episode_id=None):
        if episode_id:
            obj = self.get_object(episode_id)
            content_type = ContentType.objects.get_for_model(obj)

        else:
            obj = self.get_object(slug)
            content_type = ContentType.objects.get_for_model(obj)

        # update data with content_type and object_id
        data = request.data
        data['user'] = request.user.id
        data['content_type'] = content_type.id
        data['object_id'] = obj.id

        serializer = RatingCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)
    
    def patch(self, request, slug, episode_id=None):
        if episode_id:
            obj = self.get_object(episode_id)
            content_type = ContentType.objects.get_for_model(obj)

        else:
            obj = self.get_object(slug)
            content_type = ContentType.objects.get_for_model(obj)
            
        rating = get_object_or_404(Rating, user=request.user, content_type=content_type.id, object_id=obj.id)
        
        serializer = RatingUpdateSerializer(rating, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    def delete(self, request, slug, episode_id=None):
        if episode_id:
            obj = self.get_object(episode_id)
            content_type = ContentType.objects.get_for_model(obj)

        else:
            obj = self.get_object(slug)
            content_type = ContentType.objects.get_for_model(obj)
            
        rating = get_object_or_404(Rating, user=request.user, content_type=content_type.id, object_id=obj.id)
        rating.delete()
        
        return Response(status=HTTP_204_NO_CONTENT)


class CommentCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        raise NotImplementedError(
            'Subclasses of CommentView must define get_object method')

    def post(self, request, slug, episode_id=None):
        if episode_id:
            obj = self.get_object(episode_id)
            content_type = ContentType.objects.get_for_model(obj)

        else:
            obj = self.get_object(slug)
            content_type = ContentType.objects.get_for_model(obj)

        # update data with content_type and object_id
        data = request.data
        data['user'] = request.user.id
        data['content_type'] = content_type.id
        data['object_id'] = obj.id

        serializer = CommentCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)


class UpdateDeleteCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.user == request.user:
            serializer = CommentUpdateSerializer(comment, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.user == request.user:
            comment.delete()

            return Response(status=HTTP_204_NO_CONTENT)

        else:
            return Response(status=HTTP_401_UNAUTHORIZED)


class GenreDetailView(APIView):
    model = None
    serializer_class = None
    
    def get(self, request, genre):
        genre = get_object_or_404(Genre, slug=genre)
        
        if self.model == "movies":    
            content_list = genre.genre_movies.all()
            
        elif self.model == "shows":
            content_list = genre.genre_shows.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(content_list, request)
        serializer = self.serializer_class(page, many=True)

        data = {
            'country': genre.name,
            self.model : serializer.data,
        }

        response = Response(data)
        response['X-Total-Count'] = paginator.page.paginator.count
        response['X-Page-Size'] = paginator.page_size
        response['X-Page'] = paginator.page.number
        
        return response


class CountryDetailView(APIView):
    model = None
    serializer_class = None
    
    def get(self, request, country):
        country = get_object_or_404(Country, slug=country)
        
        if self.model == "movies":    
            content_list = country.country_movies.all()
            
        elif self.model == "shows":
            content_list = country.country_shows.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(content_list, request)
        serializer = self.serializer_class(page, many=True)

        data = {
            'genre': country.name,
            self.model : serializer.data,
        }

        response = Response(data)
        response['X-Total-Count'] = paginator.page.paginator.count
        response['X-Page-Size'] = paginator.page_size
        response['X-Page'] = paginator.page.number
        
        return response
    
    
class GenreListView(APIView):
    def get(self, request):
        movie_genres = Genre.objects.filter(genre_movies__isnull=False).distinct()
        shows_genres = Genre.objects.filter(genre_shows__isnull=False).distinct()
        
        data = {
            "movies": GenreCountryListSerializer(movie_genres, many=True).data,
            "shows": GenreCountryListSerializer(shows_genres, many=True, include_movies_count=False).data,
        }

        return Response(data)
    
    
class CountryListView(APIView):
    def get(self, request):
        movie_countries = Country.objects.filter(country_movies__isnull=False).distinct()
        shows_countries = Country.objects.filter(country_shows__isnull=False).distinct()
        
        data = {
            "movies": GenreCountryListSerializer(movie_countries, many=True).data,
            "shows": GenreCountryListSerializer(shows_countries, many=True, include_movies_count=False).data,
        }

        return Response(data)