from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CreateUserView, LoginView, ProfileView,
    GlobalProfileView, ChangePasswordView,
    CheckUsernameEmailView, ResetPasswordRequestView,
    ResetPasswordView, ResendEmailConfirmCodeView
)

app_name = "accounts"

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<int:user_id>/', GlobalProfileView.as_view(), name='global_profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('resend-code/', ResendEmailConfirmCodeView.as_view(), name='resend_code'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset_password_request'),
    path('reset-password/<uuid:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('check-username-email/', CheckUsernameEmailView.as_view(), name='check_username_email')
]