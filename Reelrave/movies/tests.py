from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Movie
from specifications.models import Genre, Country, Rating


User = get_user_model()


class MovieTest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            name="TestMovie",
            release_date="2023-06-20",
            time="02:22:32",
            content_rating="R",
            storyline="test",
            description="test",
            featured=True,
            baner="/movies/TestMovie/baners/test.jpg",
        )

        self.genre = Genre.objects.create(name="test")
        self.genre_2 = Genre.objects.create(name="test2")

        self.country = Country.objects.create(
            name="Test", flag="/countries/Test/test.jpg"
        )

        self.movie.genre.add(self.genre)

        self.movie.country_of_origin.add(self.country)

        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password=make_password("testpassword"),
        )

        return super().setUp()

    def test_movie_list(self):
        url = reverse("movies:movie_list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.movie.name)

    def test_movie_detail(self):
        url = reverse("movies:movie_detail", kwargs={"slug": self.movie.slug})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["movie"]["name"], self.movie.name)

    def test_movie_by_genre(self):
        url = reverse("movies:movie_by_genre", kwargs={"genre": self.genre.slug})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["genre"], self.genre.name)
        self.assertEqual(response.data["movies"][0]["name"], self.movie.name)

    def test_movie_by_country(self):
        url = reverse("movies:movie_by_country", kwargs={"country": self.country.slug})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country"], self.country.name)
        self.assertEqual(response.data["movies"][0]["name"], self.movie.name)
        
    def test_top_movies(self):
        content_type = ContentType.objects.get_for_model(self.movie._meta.model)
        
        Rating.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.movie.id,
            rating=10,
        )
        
        url = reverse("movies:top_movies")
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['top_movies'][0]['name'], self.movie.name)
        
    def test_top_movies_by_genre(self):
        content_type = ContentType.objects.get_for_model(self.movie._meta.model)
        
        Rating.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.movie.id,
            rating=10,
        )
        
        url = reverse("movies:top_movies_by_genre", kwargs={"genre": self.genre.slug})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['top_movies'][0]['name'], self.movie.name)
        self.assertEqual(response.data['movie_genres'][0]['name'], self.genre.name)