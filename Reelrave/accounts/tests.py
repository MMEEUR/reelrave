from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import EmailConfirm


User = get_user_model()


class RegisterTest(APITestCase):
    def setUp(self):
        url = reverse("accounts:resend_code")
        
        data = {
            "email": "test@example.com"
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.email_code = EmailConfirm.objects.get(email="test@example.com").code
        
        return super().setUp()
    
    def test_register(self):
        url = reverse("accounts:register")
        
        data = {
            "username": "testuser",
            "password": "testpassword",
            "confirm_password": "testpassword",
            "email": "test@example.com",
            "email_code": self.email_code
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password=make_password("testpassword")
        )
        
        return super().setUp()
    
    def test_login(self):
        url = reverse("accounts:login")
        
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class ProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password=make_password("testpassword")
        )
        
        return super().setUp()
    
    def test_global_profile(self):
        url = reverse("accounts:global_profile", kwargs={"user_id": self.user.id})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        
    def test_profile(self):
        access_token = RefreshToken.for_user(self.user).access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        url = reverse("accounts:profile")
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        
    def test_update_profile(self):
        access_token = RefreshToken.for_user(self.user).access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        url = reverse("accounts:profile")
        
        data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'bio': 'Test Developer',
            'date_of_birth': '2000-01-01',
            'photo': None
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)