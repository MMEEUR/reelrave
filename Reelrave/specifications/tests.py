from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase
from movies.models import Movie
from .models import Comment, Photo


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