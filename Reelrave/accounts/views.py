from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import CreateUserSerializer, ProfileSerializer
from .models import Profile


class CreateUserView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('account:profile')

        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('account:profile')
        
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid login credentials"}, status=HTTP_401_UNAUTHORIZED)

        old_refresh_tokens = RefreshToken.objects.filter(user=user)

        for token in old_refresh_tokens:
            try:
                token.blacklist()

            except TokenError:
                pass

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "refresh": str(refresh),
            "access": str(access)
        })


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user

        try:
            profile = user.profile

        except Profile.DoesNotExist:
            profile = Profile(user=user)
            profile.save()

        return profile

    def get(self, request):
        profile = self.get_object()
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
class GlobalProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), id=user_id)
        profile = user.profile
        
        data = {
            "user": user.username,
            "profile": ProfileSerializer(profile).data
        }
        
        return Response(data)