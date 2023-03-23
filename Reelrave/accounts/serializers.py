from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ValidationError, CharField
from .models import Profile
        
class CreateUserSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = get_user_model().objects.create_user(**validated_data)
        return user

class CommentProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('photo',)
    
class UserCommentSerializer(ModelSerializer):
    profile = CommentProfileSerializer(read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'profile')