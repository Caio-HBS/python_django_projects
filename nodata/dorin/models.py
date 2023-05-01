from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    pfp = models.ImageField(upload_to="")
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=35)
    custom_slug_profile = models.SlugField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.user.username})"


class Post(models.Model):
    parent_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    post_text = models.TextField(max_length=1000, null=False, blank=False)
    image = models.ImageField(upload_to="")
    publication_date_post = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.title} ({self.publication_date_post})"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500, null=False, blank=False)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    publication_date_comment = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in response of {self.parent_post.user} ({self.parent_post.title})"