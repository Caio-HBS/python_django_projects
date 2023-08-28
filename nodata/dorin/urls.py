from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login_page"),
    path("logout/", views.logout_view, name="logout_page"),
    path("register/", views.RegisterView.as_view(), name="register_page"),
    path("feed/", views.decorated_feed_view, name="feed_page"),
    path("profile/<slug:custom_slug_profile>/", views.single_profile_view, name="profile_page"),
    path("post/<slug:post_slug>/", views.single_post_view, name="post_page"),
    path("discover/", views.discover_view, name="discover_page"),
    path("about-us/", views.about_us_view, name="about_us_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)