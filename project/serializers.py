from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import Profile

from .models import Project, Review


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username")

    class Meta:
        model = Project
        fields = ["id", "title", "about", "image_1", "created", "owner"]


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    review_user_image = serializers.SerializerMethodField()

    class Meta:
        model = Review
        exclude = ["project", "active"]

    def get_review_user_image(self, obj):
        profile = Profile.objects.get(user=obj.review_user)
        return profile.profile_pic.url


class ProjectDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    contributors = ContributorSerializer(many=True, read_only=True)
    user_liked = serializers.SerializerMethodField()
    owner = ContributorSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        exclude = ["likes"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_user_liked(self, obj):
        request = self.context.get("request", None)

        if request:
            if request.user in obj.likes.all():
                return True
            else:
                return False
        return False
