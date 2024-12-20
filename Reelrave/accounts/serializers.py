from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
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
        code = attrs['email_code']
           
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"error": "Passwords must match."})
        
        validate_password(attrs['password'])
        
        try:
            EmailConfirm.objects.get(email=email, code=code, expires__gte=timezone.now())
            
        except EmailConfirm.DoesNotExist:
            raise serializers.ValidationError({"error": "Confirm code is incorrect."})
        
        validated_data.pop('confirm_password')
        validated_data.pop('email_code')
            
        return validated_data
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        validated_data.pop('email_code', None)

        user = User(**validated_data)
        
        if password:
            user.set_password(password)
            
        user.save()
        
        return user
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        
        user = authenticate(username=attrs['username'], password=attrs['password'])
        
        if not user:
            raise serializers.ValidationError({"error": "Invalid login credentials"})
        
        validated_data['user'] = user
        
        return validated_data

        
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'date_of_birth', 'photo')
        
        
class UserProfileChangeSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    photo = serializers.URLField(required=False)
    
    class Meta:
        model = User
        fields = ('bio', 'date_of_birth', 'photo')


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
            raise serializers.ValidationError({"error": "Incorrect password."})
        
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError({"error": "New password should be different from the old password."})
        
        return super().validate(attrs)
    
    
class PasswordResetRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        
        try:
            user = User.objects.get(username=attrs['username'])
            
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User does not exist."})
        
        if user.is_staff:
            raise serializers.ValidationError({"error": "User does not exist."})

        if PasswordReset.objects.filter(user=user, expires__gte=timezone.now()).exists():
            raise serializers.ValidationError({"error": "You must wait 2 minutes before requesting resend code."})
        
        validated_data['user'] = user
        
        return validated_data
    
    
class ResendEmailConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"error": "This email already exists."})
            
        return validated_data