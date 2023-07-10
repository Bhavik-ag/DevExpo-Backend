from django.urls import path

from .views import (
    ProjectCreate,
    ProjectDetail,
    ProjectLikeView,
    ProjectList,
    ReviewCreate,
)

urlpatterns = [
    path("", ProjectList.as_view(), name="project-list"),
    path("create/", ProjectCreate.as_view(), name="project-create"),
    path("<int:pk>/review/", ReviewCreate.as_view(), name="review-create"),
    path("<int:pk>/", ProjectDetail.as_view(), name="project-detail"),
    path("<int:pk>/like/", ProjectLikeView.as_view(), name="project-like"),
]
