from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login_page"),
    path("logout/", views.logout_view, name="logout_page"),
    path("register/", views.register_view, name="register_page"),
    path("feed/", views.feed_view, name="feed_page"),
    path("feed/new-post/", views.new_post_view, name="new_post_page"),
    path("profile/<slug:custom_slug_profile>/", views.single_profile_view, name="profile_page"),
    path("post/<slug:post_slug>/", views.single_post_view, name="post_page"),
    path("discover/", views.discover_view, name="discover_page")
]
