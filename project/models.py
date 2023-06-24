from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    
    #short description    
    about = models.TextField(max_length=100, blank=True)
    
    #long description
    description = models.TextField(max_length=1000, blank=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    demo_link = models.URLField(max_length=100,blank=True)  
    repo_link = models.URLField(max_length=100, blank=True)
    
    contributors = models.ManyToManyField(User, related_name='contributors', blank=True)
    
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    image_1 = models.ImageField(upload_to='project_images', blank=True)
    image_2 = models.ImageField(upload_to='project_images', blank=True)
    image_3 = models.ImageField(upload_to='project_images', blank=True)
    image_4 = models.ImageField(upload_to='project_images', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
