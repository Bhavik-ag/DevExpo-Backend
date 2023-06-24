from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profiles', null=True, default='v1687582654/profiles/user-default.jpg')
    
    github = models.URLField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=100, blank=True)
    twitter = models.URLField(max_length=100, blank=True)
    website = models.URLField(max_length=100, blank=True)
