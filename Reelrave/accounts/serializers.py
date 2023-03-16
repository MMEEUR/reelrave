from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from .models import Profile

class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username',)

class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        exclude = ('id',)
        
class UserCommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ('user', 'photo')