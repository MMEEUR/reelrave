from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CreateUserView, LoginView, ProfileView

app_name = "account"

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]