from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserCreateSerializer, GlobalProfileSerializer, UserProfileSerializer,
    ChangePasswordSerializer
)
from specifications.serializers import WatchListSerializer, ActivitySerializer
from .tasks import send_welcome_email


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
        user = get_object_or_404(get_user_model(), id=user_id)
        
        if user.is_staff:
            
            raise NotFound()

        serializer = GlobalProfileSerializer(user)
        
        return Response(serializer.data)
    
    
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        new_password = serializer.validated_data.get('new_password')
        old_password = serializer.validated_data.get('old_password')
        
        if not check_password(old_password, user.password):
            
            return Response({"old_password": "Incorrect password."}, HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({"detail": "Password changed successfully."})