from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsProjectUserOrReadOnly

class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectUserOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = ProjectSerializer(instance,context={'request': request})
        return Response(serializer.data)
    
class ProjectLikeView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user in instance.likes.all():
            instance.likes.remove(user)
        else:
            instance.likes.add(user)
        instance.save()
        serializer = ProjectSerializer(instance,context={'request': request})
        return Response(serializer.data)
    
