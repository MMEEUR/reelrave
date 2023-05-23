from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserCreateSerializer, GlobalProfileSerializer, UserProfileSerializer,
    ChangePasswordSerializer, PasswordResetRequestSerializer,
    ValidatePasswordSerializer
)
from specifications.serializers import WatchListSerializer, ActivitySerializer
from .models import PasswordReset
from .tasks import send_welcome_email


User = get_user_model()


class CreateUserView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:profile')

        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        send_welcome_email.delay(email=request.data['email'], username=request.data['username'])

        return Response(serializer.data, status=HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid login credentials"}, status=HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        watchlist = user.watchlist.all().values('content_type', 'object_id')
        ratings = user.user_ratings.all().values('content_type', 'object_id', 'rating')
        
        return Response({
            "refresh": str(refresh),
            "access": str(access),
            "activity": {
                "watchlist": ActivitySerializer(watchlist, many=True).data,
                "ratings": ActivitySerializer(ratings, many=True).data,
            }
        })


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):    
        watchlist = request.user.watchlist.all()
        
        data = {
            "user": UserProfileSerializer(request.user).data,
            "watchlist": WatchListSerializer(watchlist, many=True).data,
        }

        return Response(data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    
class GlobalProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        if user.is_staff:
            
            raise NotFound()

        serializer = GlobalProfileSerializer(user)
        
        return Response(serializer.data)
    
    
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        
        new_password = serializer.validated_data.get('new_password')
        
        user = request.user
        user.set_password(new_password)
        user.save()
        
        return Response({"detail": "Password changed successfully."})

    
class CheckUsernameEmailView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        data = {}

        if username:
            if User.objects.filter(username=username).exists():
                data['username'] = True

        if email:
            if User.objects.filter(email=email).exists():
                data['email'] = True

        return Response(data)
    
    
class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data["username"]
        user = User.objects.get(username=username)

        token = PasswordReset.objects.create(user=user).token
        
        reset_password_url = reverse('accounts:reset_password', kwargs={'token': token})

        subject = "Password Reset"
        message = f"Click the following link to reset your password: {reset_password_url}"
        from_email = "admin@example.com"
        to_email = user.email
        
        send_mail(subject, message, from_email, [to_email], fail_silently=False)

        return Response({"detail": "Password reset email has been sent."})
    
    
class ResetPasswordView(APIView):
    def post(self, request, token):
        try:
            password_reset = PasswordReset.objects.get(token=token)
            
        except PasswordReset.DoesNotExist:
            
            raise NotFound()   
        
        user = password_reset.user
        
        serializer = ValidatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        password = serializer.validated_data["new_password"]
        
        user.set_password(password)
        user.save()
        
        PasswordReset.objects.filter(user=user).delete()
        
        return Response({"detail": "Password has been reset successfully."})