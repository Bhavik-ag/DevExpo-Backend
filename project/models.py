from django.db import models

class Project(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250, blank=True)
    
    demo_link = models.URLField(max_length=100,blank=True)  
    repo_link = models.URLField(max_length=100, blank=True)
    
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    image_1 = models.FileField(upload_to='project_images', blank=True)
            
    created = models.DateTimeField(auto_now_add=True)
    
    
