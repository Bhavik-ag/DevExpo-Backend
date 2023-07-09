from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from user.models import Profile

from .permissions import IsProfileOwner, IsProfileUserOrReadOnly
from .serializers import RegisterUserSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']

            if '@' in request.data['username']:
                user = User.objects.get(email=request.data['username'])
            else:
                user = User.objects.get(username=request.data['username'])
                
            response.data['username'] = user.username
            response.data['name'] = user.get_full_name()
            profile = Profile.objects.get(user=user)
            response.data['profile_image'] = profile.profile_pic.url
            
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE          
            )
            
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE    
            )
        
        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            request.data['refresh'] = refresh_token
            
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data['access']
            
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE          
            )
            
        return response
    
class ProfileDetail(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProfileUserOrReadOnly]
    lookup_field = 'username'   
    
class ProfileUpdate(APIView):   
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsProfileOwner]

    def patch(self, request, username, format=None):
        
        if request.user != User.objects.get(username=username):
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        
        try:
        
            if request.data.get('first_name'):
                user.first_name = request.data['first_name']
            
            if request.data.get('last_name'):
                user.last_name = request.data['last_name']
                
            user.save()
            
            if request.data.get('profile_pic'):
                profile.profile_pic = request.data['profile_pic']
                
            if request.data.get('bio'):
                profile.bio = request.data['bio']
            
            if request.data.get('github'):
                profile.github = request.data['github']
                
            if request.data.get('linkedin'):
                profile.linkedin = request.data['linkedin']
                
            if request.data.get('twitter'):
                profile.twitter = request.data['twitter']
                
            if request.data.get('website'):
                profile.website = request.data['website']
                
            profile.save()
            
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        profile = Profile.objects.get(user=user)
        
        token = RefreshToken.for_user(user)
        
        data = {
            'refresh': str(token),
            'access': str(token.access_token),
            'username': user.username,
            'name': user.get_full_name(),
            'profile_image': profile.profile_pic.url
        }
                
        return Response(data, status=status.HTTP_201_CREATED)
    
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
                
        if access_token:
            request.data['token'] = access_token
        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                try:
                    token = AccessToken(access_token)
                    user_id = token.payload['user_id']
                    user = User.objects.get(id=user_id)
                    response.data['username'] = user.username
                    response.data['name'] = user.get_full_name()
                    profile = Profile.objects.get(user=user)
                    response.data['profile_image'] = profile.profile_pic.url
                except Exception as e:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            return response
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
             
class LogoutUser(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        response.delete_cookie('access')
        response.delete_cookie('refresh')
         
        response.data = {
            'message': 'success'
        }
        
        return response