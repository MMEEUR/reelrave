from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import EmailConfirm


class AccountTestCase(APITestCase):
    def setUp(self):
        self.email_code = None
        self.refresh_token = None
        self.user_id = None
        
        return super().setUp()
    
    def test_send_email_code(self):
        url = reverse("accounts:resend_code")
        
        data = {
            'email': 'testuser@example.com'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.email_code = EmailConfirm.objects.get(email='testuser@example.com').code
        
    
    def test_register(self):
        url = reverse("accounts:register")
        
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'code': self.email_code
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.user_id = response.data['id']
        
    def test_login(self):
        url = reverse("accounts:login")
        
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.refresh_token = response.data['refresh']
        
    def test_token_refresh(self):
        url = reverse("accounts:token_refresh")
        
        data = {
            'refresh': self.refresh_token
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.access_token = response.data['access']