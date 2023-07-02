from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile
from project.serializers import ProjectSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user', 'id']
        
class UserSerializer(serializers.ModelSerializer):    
    projects = ProjectSerializer(many=True, read_only=True)
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name','profile','projects']
        
    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = instance.profile
            profile_serializer = ProfileSerializer(profile, data=profile_data, partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()
            
        return super().update(instance, validated_data)
        
class RegisterUserSerializer(serializers.ModelSerializer):
    
    # Make email compulsory
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['id','username', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        account = User(email=self.validated_data['email'], username= self.validated_data['username'])
        
        account.set_password(self.validated_data['password'])
        account.save()
        
        # Create a profile for the user
        profile = Profile(user=account)
        profile.save()
        
        return account

    
