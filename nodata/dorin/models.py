from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    pfp = models.ImageField(upload_to="profile_pictures")
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=35)
    custom_slug_profile = models.SlugField(max_length=15)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.user.username})"


class Post(models.Model):
    parent_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    post_text = models.TextField(max_length=1000, null=False, blank=False)
    image = models.ImageField(upload_to="post_pictures", null=True)
    publication_date_post = models.DateTimeField(auto_now_add=True)
    post_slug = models.SlugField(max_length=15)

    def __str__(self):
        return f"{self.parent_profile.user}: {self.title} ({self.publication_date_post})"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500, null=False, blank=False)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    publication_date_comment = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in response of {self.parent_post.parent_profile} ({self.parent_post.title})"
    

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.IntegerField(validators=[MinValueValidator(0)])

def __str__(self):
        return f"{self.likes} likes on post {self.parent_post}"