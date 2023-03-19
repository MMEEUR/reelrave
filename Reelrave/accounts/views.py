from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CreateUserSerializer

# Create your views here.
class CreateUserView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({"error": "Invalid login credentials"}, status=HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        return Response({
            "refresh": str(refresh),
            "access": str(access)
        })