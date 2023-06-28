from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Project, Review
from .serializers import ProjectSerializer, ProjectDetailSerializer, ReviewSerializer
from .permissions import IsProjectUserOrReadOnly

class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
class ProjectCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsProjectUserOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance,context={'request': request})
        return Response(serializer.data)
    
class ProjectLikeView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user in instance.likes.all():
            instance.likes.remove(user)
        else:
            instance.likes.add(user)
        instance.save()
        serializer = ProjectDetailSerializer(instance,context={'request': request})
        return Response(serializer.data)
    
class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes  = [IsAuthenticated]
    lookup_field = 'project.id'
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        
        project = Project.objects.get(id = self.kwargs.get('pk'))
        reviews = Review.objects.filter(project=project)
        
        return Response(ReviewSerializer(reviews, many=True).data, status=status.HTTP_201_CREATED)
        
    
    def perform_create(self, serializer):
        project = Project.objects.get(id = self.kwargs.get('pk'))
        serializer.save(review_user=self.request.user, project=project)
            