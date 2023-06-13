from rest_framework import status
from rest_framework.test import APITestCase


class HomeTest(APITestCase):
    def test_home_page(self):
        data = {
            "featured_movies": [],
            "latest_trailers": [],
            "latest_episodes": [],
            "latest_movies": [],
        }

        response = self.client.get("")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)