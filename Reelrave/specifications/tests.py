from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase
from movies.models import Movie
from .models import Comment, Photo, Video, Genre, Country


User = get_user_model()


class PhotoTest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            name="TestMovie",
            release_date="2023-06-20",
            time="02:22:32",
            content_rating="R",
            storyline="test",
            description="test",
            featured=True,
            baner="files/movies/TestMovie/baners/test.jpg",
        )

        self.photo = Photo.objects.create(
            title="test",
            content_type=ContentType.objects.get_for_model(self.movie._meta.model),
            object_id=self.movie.id,
            image="files/movies/TestMovie/photo/test.jpg",
        )

        return super().setUp()

    def test_photos(self):
        url = reverse("spec:photos")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.photo.title)


class VideoTest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            name="TestMovie",
            release_date="2023-06-20",
            time="02:22:32",
            content_rating="R",
            storyline="test",
            description="test",
            featured=True,
            baner="files/movies/TestMovie/baners/test.jpg",
        )

        self.video = Video.objects.create(
            title="test",
            content_type=ContentType.objects.get_for_model(self.movie._meta.model),
            object_id=self.movie.id,
            video="files/movies/TestMovie/video/test.jpg",
            is_trailer=True,
        )

        return super().setUp()

    def test_videos(self):
        url = reverse("spec:videos")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.video.title)


class GenreTest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            name="TestMovie",
            release_date="2023-06-20",
            time="02:22:32",
            content_rating="R",
            storyline="test",
            description="test",
            featured=True,
            baner="files/movies/TestMovie/baners/test.jpg",
        )

        self.genre = Genre.objects.create(name="test")
        self.genre_2 = Genre.objects.create(name="test2")

        self.movie.genre.add(self.genre)
        self.movie.genre.add(self.genre_2)

        return super().setUp()

    def test_genres(self):
        url = reverse("spec:genres")

        response = self.client.get(url)

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["genre_movies"][0]["name"], self.genre.name)
        self.assertEqual(response.data["genre_movies"][1]["name"], self.genre_2.name)
        self.assertEqual(response.data["genre_movies"][0]["movies_count"], 1)
        self.assertEqual(response.data["genre_movies"][1]["movies_count"], 1)


class CountryTest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            name="TestMovie",
            release_date="2023-06-20",
            time="02:22:32",
            content_rating="R",
            storyline="test",
            description="test",
            featured=True,
            baner="files/movies/TestMovie/baners/test.jpg",
        )

        self.country = Country.objects.create(name="test")
        self.country_2 = Country.objects.create(name="test2")

        self.movie.country_of_origin.add(self.country)
        self.movie.country_of_origin.add(self.country_2)

    def test_countries(self):
        url = reverse("spec:countries")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country_movies"][0]["name"], self.country.name)
        self.assertEqual(response.data["country_movies"][1]["name"], self.country_2.name)
        self.assertEqual(response.data["country_movies"][0]["movies_count"], 1)
        self.assertEqual(response.data["country_movies"][1]["movies_count"], 1)