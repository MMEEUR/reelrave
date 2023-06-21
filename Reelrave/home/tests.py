from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase
from movies.models import Movie


class HomeTest(APITestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

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

        return super().setUp()

    def test_home_page(self):
        response = self.client.get("")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["featured_movies"][0]["id"], self.movie.id)
        self.assertEqual(response.data["latest_movies"][0]["id"], self.movie.id)

    def test_search(self):
        response = self.client.get(f"/search/?q={self.movie.name}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["query"], "TestMovie")
        self.assertEqual(response.data["result"][0]["object_id"], self.movie.id)