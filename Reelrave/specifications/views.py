from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from .models import Genre, Country, Comment, CommentLikeDisLike, Rating, WatchList
from .serializers import (
    GenreSerializer, CountrySeralizer,
    RatingCreateSerializer, RatingUpdateSerializer,
    CommentUpdateSerializer, CommentCreateSerializer,
    CommentLikeDisLikeSerializer, CommentLikeDisLikeUpdateSerializer,
    WatchListAddSerializer
)
from movies.serializers import MovieListSerializer
from shows.serializers import ShowListSerializer


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


class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        return Response(serializer.data)


class GenreDetailView(APIView):
    def get(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        movies = genre.genre_movies.all()
        shows = genre.genre_shows.all()

        serializer1 = MovieListSerializer(movies, many=True)
        serializer2 = ShowListSerializer(shows, many=True)

        data = {
            'genre': genre.name,
            'movies': serializer1.data,
            'shows': serializer2.data
        }

        return Response(data)


class CountryListView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySeralizer(countries, many=True)

        return Response(serializer.data)


class CountryDetailView(APIView):
    def get(self, request, slug):
        country = get_object_or_404(Country, slug=slug)
        movies = country.country_movies.all()
        shows = country.country_shows.all()

        serializer1 = MovieListSerializer(movies, many=True)
        serializer2 = ShowListSerializer(shows, many=True)

        data = {
            'country': country.name,
            'movies': serializer1.data,
            'shows': serializer2.data
        }

        return Response(data)