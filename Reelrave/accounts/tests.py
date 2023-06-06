from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import EmailConfirm


User = get_user_model()


class RegisterTest(APITestCase):
    def setUp(self):
        url = reverse("accounts:resend_code")
        
        data = {
            "email": "test@example.com"
        }
        
        response = self.client.post(url, data)
        
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
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)