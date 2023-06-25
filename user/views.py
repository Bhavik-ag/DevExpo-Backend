from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, RegisterUserSerializer
from .permissions import IsProfileOwnerOrReadOnly
    
class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]
    lookup_field = 'username'
    
    
class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        
        token = RefreshToken.for_user(user)
        
        data = {
            'refresh': str(token),
            'access': str(token.access_token),
        }
                
        return Response(data, status=status.HTTP_201_CREATED)
    
    