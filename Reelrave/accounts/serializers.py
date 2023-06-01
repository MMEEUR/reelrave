from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import PasswordReset, EmailConfirm


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    email_code = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'confirm_password', 'email_code'
        )
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        
        email = attrs['email']
        code = attrs.get('email_code')
           
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        
        try:
            EmailConfirm.objects.get(email=email, code=code, expires__gte=timezone.now())
            
        except EmailConfirm.DoesNotExist:
            raise serializers.ValidationError("Confirm code is incorrect.")
        
        validated_data.pop('confirm_password')
        validated_data.pop('email_code')
            
        return validated_data

        
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'date_of_birth', 'photo')


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'photo', 'get_absolute_url')
        
        
class GlobalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'photo', 'date_of_birth', 'bio')
        
        
class ValidatePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
        
    def validate(self, attrs):      
            validate_password(attrs['new_password'])
            
            return super().validate(attrs)
        
        
class ChangePasswordSerializer(ValidatePasswordSerializer):
    old_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        user = self.context['user']
        
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Incorrect password.")
        
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError("New password should be different from the old password.")
        
        return super().validate(attrs)
    
    
class PasswordResetRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        
        user = User.objects.get(username=attrs['username'])
        
        if not user or user.is_staff:
            raise serializers.ValidationError("User does not exist.")

        if PasswordReset.objects.filter(user=user, expires__gte=timezone.now()).count() >= 3:
            raise serializers.ValidationError("Too many requests.")
        
        validated_data['user'] = user
        
        return validated_data
    
    
class ResendEmailConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("This email already exists.")
            
        return validated_data