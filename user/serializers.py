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
