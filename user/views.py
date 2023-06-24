from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User

from .models import Profile
from .serializers import ProfileSerializer,UserSerializer

class ProfileList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ProfileDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer