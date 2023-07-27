from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.ProfileListAPIView.as_view(), name='api_profile_index'),
    path('profiles/<int:pk>/', views.ProfileDetailAPIView.as_view(), name='api_profile_detail'),
    path('profiles/<int:pk>/update/', views.ProfileUpdateAPIView.as_view(), name='api_profile_update'),
    path('profiles/<int:pk>/delete/', views.ProfileDestroyAPIView.as_view(), name='api_profile_delete'),
    path('profiles/<int:pk>/posts/', views.PostListCreateAPIView.as_view(), name='api_post_list_create'),
]
