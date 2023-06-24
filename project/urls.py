from django.urls import path

from .views import (ProjectList,ProjectDetail,ProjectLikeView)

urlpatterns = [
    path('', ProjectList.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('<int:pk>/like/', ProjectLikeView.as_view(), name='project-like'),
]
