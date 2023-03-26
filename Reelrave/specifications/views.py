from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from .models import Genre, Country, Comment
from .serializers import GenreSerializer, CountrySeralizer, CommentUpdateSerializer, CommentCreateSerializer
from movies.serializers import MovieListSerializer
from shows.serializers import ShowListSerializer


class CommentCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, slug):
        raise NotImplementedError(
            'Subclasses of CommentView must define get_object method')

    def post(self, request, slug):
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

    def put(self, request, comment_id):
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