from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=False, null=False)
    pfp = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=35)
    custom_slug_profile = models.SlugField(max_length=15, unique=True)
    friends = models.ManyToManyField('self', blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return f"dorinsocialapi/profiles/{self.pk}/"

    @property    
    def endpoint(self):
        return self.get_absolute_url()
        
    def get_custom_slug_profile(self):
        return f"{reverse('profile_page', kwargs={'custom_slug_profile': self.custom_slug_profile})}"
    
    @property
    def endpoint_custom_slug(self):
        return self.get_custom_slug_profile()


    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.user.username})"


class Post(models.Model):
    parent_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50, null=False, blank=False)
    post_text = models.TextField(max_length=1000, null=False, blank=False)
    image = models.ImageField(upload_to="post_pictures", null=True)
    publication_date_post = models.DateTimeField(auto_now_add=True)
    post_slug = models.SlugField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.parent_profile.user}: {self.title} ({self.publication_date_post})"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500, null=False, blank=False)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    publication_date_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in response of {self.parent_post.parent_profile} ({self.parent_post.title})"
    

    