from django.urls import path
from .views import (ProfileDetail, RegisterUser)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('register/', RegisterUser.as_view(), name='register'),
]