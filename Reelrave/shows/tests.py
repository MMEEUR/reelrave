from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Show, Season, Episode
from specifications.models import Genre, Country, Rating


User = get_user_model()


class ShowTest(APITestCase):
    def setUp(self):
        self.show = Show.objects.create(
            name="TestMovie",
            release_date="2023-06-20",
            content_rating="TV-MA",
            storyline="test",
            description="test",
            baner="files/movies/TestMovie/baners/test.jpg",
        )
        
        self.season = Season.objects.create(
            show = self.show,
            number = 1
        )
        
        self.episode = Episode.objects.create(
            season = self.season,
            number = 1,
            name="TestMovie",
            release_date="2023-06-20",
            content_rating="TV-MA",
            time="02:22:32",
            storyline="test",
            description="test",
            baner="files/movies/TestMovie/baners/test.jpg",
        )

        self.genre = Genre.objects.create(name="test")
        self.genre_2 = Genre.objects.create(name="test2")

        self.country = Country.objects.create(
            name="Test", flag="/countries/Test/test.jpg"
        )

        self.show.genre.add(self.genre)
        self.episode.genre.add(self.genre)

        self.show.country_of_origin.add(self.country)

        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password=make_password("testpassword"),
        )
        
        access_token = RefreshToken.for_user(self.user).access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        return super().setUp()

    def test_show_list(self):
        url = reverse("shows:show_list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.show.name)

    def test_show_detail(self):
        url = reverse("shows:show_detail", kwargs={"slug": self.show.slug})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["show"]["name"], self.show.name)

    def test_show_by_genre(self):
        url = reverse("shows:show_by_genre", kwargs={"genre": self.genre.slug})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["genre"], self.genre.name)
        self.assertEqual(response.data["shows"][0]["name"], self.show.name)

    def test_show_by_country(self):
        url = reverse("shows:show_by_country", kwargs={"country": self.country.slug})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country"], self.country.name)
        self.assertEqual(response.data["shows"][0]["name"], self.show.name)
        
    def test_top_shows(self):
        content_type = ContentType.objects.get_for_model(self.show._meta.model)
        
        Rating.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.show.id,
            rating=10
        )
        
        url = reverse("shows:top_shows")
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['top_shows'][0]['name'], self.show.name)
        
    def test_top_shows_by_genre(self):
        content_type = ContentType.objects.get_for_model(self.show._meta.model)
        
        Rating.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=self.show.id,
            rating=10
        )
        
        url = reverse("shows:top_shows_by_genre", kwargs={"genre": self.genre.slug})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['top_shows'][0]['name'], self.show.name)
        self.assertEqual(response.data['show_genres'][0]['name'], self.genre.name)
        
    def test_show_create_comment(self):
        url = reverse("shows:show_create_comment", kwargs={"slug": self.show.slug})
        
        data = {
            "body": "Test Comment"
        }
        
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.show.comments.first().body, data['body'])
        self.assertEqual(self.show.comments.first().user, self.user)
        
    def test_show_rating(self):
        url = reverse("shows:show_rating", kwargs={"slug": self.show.slug})
        
        response = self.client.post(url, {"rating": 10}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.show.ratings.first().rating, 10)
        self.assertEqual(self.show.ratings.first().user, self.user)
        
        response = self.client.post(url, {"rating": 10}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.patch(url, {"rating": 9}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.show.ratings.first().rating, 9)
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.show.ratings.exists(), False)
        
    def test_show_watchlist(self):
        url = reverse("shows:show_watchlist", kwargs={"slug": self.show.slug})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.show.watchlist.first().user, self.user)
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.show.watchlist.exists(), False)
        
        
class EpisodeTest(APITestCase):
    def setUp(self):
        self.show = Show.objects.create(
            name="TestMovie",
            release_date="2023-06-20",
            content_rating="TV-MA",
            storyline="test",
            description="test",
            baner="files/movies/TestMovie/baners/test.jpg",
        )
        
        self.season = Season.objects.create(
            show = self.show,
            number = 1
        )
        
        self.episode = Episode.objects.create(
            season = self.season,
            number = 1,
            name="TestMovie",
            release_date="2023-06-20",
            content_rating="TV-MA",
            time="02:22:32",
            storyline="test",
            description="test",
            baner="files/movies/TestMovie/baners/test.jpg",
        )

        self.genre = Genre.objects.create(name="test")
        self.genre_2 = Genre.objects.create(name="test2")

        self.country = Country.objects.create(
            name="Test", flag="/countries/Test/test.jpg"
        )

        self.show.genre.add(self.genre)
        self.episode.genre.add(self.genre)

        self.show.country_of_origin.add(self.country)

        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password=make_password("testpassword"),
        )
        
        access_token = RefreshToken.for_user(self.user).access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        return super().setUp()
    
    def test_episode_list(self):
        url = reverse("shows:episode_list", kwargs={"slug": self.show.slug})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['show'], self.show.name)
        self.assertEqual(response.data['seasons'][0]['number'], self.season.number)
        self.assertEqual(response.data['seasons'][0]['episodes'][0]['name'], self.episode.name)
        
    def test_episode_detail(self):
        url = reverse("shows:episode_detail", kwargs={"slug": self.show.slug, "episode_id": self.episode.id})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['show'], self.show.name)
        self.assertEqual(response.data['number'], f"S{self.season.number}.E{self.episode.number}")
        self.assertEqual(response.data['episode']['name'], self.episode.name)
        
    def test_episode_create_comment(self):
        url = reverse("shows:episode_create_comment", kwargs={"slug": self.show.slug, "episode_id": self.episode.id})
        
        data = {
            "body": "Test Comment"
        }
        
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.episode.comments.first().body, data['body'])
        self.assertEqual(self.episode.comments.first().user, self.user)
        
    def test_episode_rating(self):
        url = reverse("shows:episode_rating", kwargs={"slug": self.show.slug, "episode_id": self.episode.id})
        
        response = self.client.post(url, {"rating": 10}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.episode.ratings.first().rating, 10)
        self.assertEqual(self.episode.ratings.first().user, self.user)
        
        response = self.client.post(url, {"rating": 10}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.patch(url, {"rating": 9}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.episode.ratings.first().rating, 9)
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.episode.ratings.exists(), False)
        
    def test_episode_watchlist(self):
        url = reverse("shows:episode_watchlist", kwargs={"slug": self.show.slug, "episode_id": self.episode.id})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.episode.watchlist.first().user, self.user)
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.episode.watchlist.exists(), False)