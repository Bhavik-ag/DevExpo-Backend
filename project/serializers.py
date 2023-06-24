from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name']


class ProjectSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    contributors = ContributorSerializer(many=True, read_only=True)
    user_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        exclude = ['likes']
        
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_user_liked(self, obj):
        request = self.context.get('request', None)
        if request:
            if request.user in obj.likes.all():
                return True
            else:
                return False
        return False
