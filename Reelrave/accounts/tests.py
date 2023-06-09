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
        
        access_token = RefreshToken.for_user(self.user).access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        return super().setUp()
    
    def test_global_profile(self):
        url = reverse("accounts:global_profile", kwargs={"user_id": self.user.id})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        
    def test_profile(self):
        url = reverse("accounts:profile")
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        
    def test_update_profile(self): 
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
        
        
class RefreshTokenTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password=make_password("testpassword")
        )
        
        return super().setUp()
    
    def test_refresh_token(self):
        refresh_token = RefreshToken.for_user(self.user)
        
        url = reverse("accounts:token_refresh")
        
        data = {
            "refresh": str(refresh_token)
        }
        
        response = self.client.post(url, data)
        
        authentication = JWTAuthentication()
        validated_token = authentication.get_validated_token(response.data['access'])
        user = authentication.get_user(validated_token)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, user.username)
        
        
class ChangePasswordTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password=make_password("testpassword")
        )
        
        access_token = RefreshToken.for_user(self.user).access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        return super().setUp()
    
    def test_change_password(self):
        url = reverse("accounts:change_password")
        
        data = {
            "old_password": "testpassword",
            "new_password": "testpassword1"
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_wrong_old_password(self):
        url = reverse("accounts:change_password")
        
        data = {
            "old_password": "testpassword2",
            "new_password": "testpassword1"
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_same_passwords(self):
        url = reverse("accounts:change_password")
        
        data = {
            "old_password": "testpassword",
            "new_password": "testpassword"
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)