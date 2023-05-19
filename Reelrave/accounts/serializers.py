from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email', 'password', 'confirm_password'
        )
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = get_user_model().objects.create_user(**validated_data)

        return user

        
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'bio', 'date_of_birth', 'photo')


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'photo', 'get_absolute_url')
        
        
class GlobalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'photo', 'date_of_birth', 'bio')
        
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        user = self.context['user']
        
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Incorrect password.")
        
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError("New password should be different from the old password.")
        
        validate_password(attrs['new_password'])
        
        return super().validate(attrs)