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
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name','profile','projects']
        
class RegisterUserSerializer(serializers.ModelSerializer):
    
    # Make email compulsory
    email = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['id','username', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        account = User(email=self.validated_data['email'], username= self.validated_data['username'])
        
        account.set_password(self.validated_data['password'])
        account.save()
        
        # Create a profile for the user
        profile = Profile(user=account)
        profile.save()
        
        return account

    
