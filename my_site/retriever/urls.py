from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index_page"),
    path("tweets/", views.twitter_view, name="tweets_page"),
    path("yt-videos/", views.youtube_view, name="yt_videos_page"),
    path("insta-posts/", views.instagram_view, name="insta_posts_page"),
]
