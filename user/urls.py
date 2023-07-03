from django.urls import path
from .views import (ProfileDetail, RegisterUser, CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, LogoutUser, ProfileUpdate)


urlpatterns = [
    path('profile/<str:username>/', ProfileDetail.as_view(), name='profile-detail'),
    path('profile/<str:username>/update/',ProfileUpdate.as_view(),name='profile-update'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('verify/', CustomTokenVerifyView.as_view(), name='verify'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]   