from django.db import models


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=50, null=False)
    url = models.URLField(max_length=200, null=False)
    upload_date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    description_excerpt = models.CharField(max_length=150, null=False, blank=False)
    channel_name = models.CharField(max_length=50, null=False, blank=True)
    thumbnail = models.URLField(max_length=300, null=False, blank=False)
    profile_image = models.URLField(max_length=300, null=False, blank=False)
    
    def __str__(self):
        return f"{self.title}, by: {self.channel_name}"


class YouTubeVideoKeyword(models.Model):
    yt_video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f"{self.keyword} - {self.yt_video.channel_name}, {self.yt_video.title}(parent video)"

class InstagramPost(models.Model):
    ig_username = models.CharField(max_length=50, null=False)
    ig_display_name = models.CharField(max_length=50, null=False)
    caption = models.CharField(max_length=500, null=False)
    comments_count = models.CharField(max_length=20, null=False)
    likes_count = models.CharField(max_length=20, null=False)
    post_time = models.DateField(auto_now=False, auto_now_add=False, null=False)
    profile_picture = models.URLField(max_length=200, null=False)
    post_url = models.URLField(max_length=200, null=False)
    media_type = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f"{self.ig_username}: {self.caption} ({self.post_time})"
    
    
class InstagramPostImage(models.Model):
    instagram_post = models.ForeignKey(InstagramPost, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=300, null=False)

    def __str__(self):
        return f"{self.instagram_post.ig_username}: {self.instagram_post.caption}(parent post)"


class Tweet(models.Model):
    user = models.CharField(max_length=50, null=False, blank=False)
    display_name = models.CharField(max_length=100, null=False, blank=False)
    profile_image = models.URLField(max_length=500, null=False)
    tweet_text = models.CharField(max_length=280, null=False)
    image = models.ImageField(upload_to="posts_images/twitter", blank=True)
    url = models.URLField(unique=True, max_length=500, null=False)
    post_date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    
    def __str__(self):
        return f"@{self.user}: {self.tweet_text} ({self.post_date})"
    

class TweetKeyword(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f"{self.keyword} - {self.tweet.user}, {self.tweet.tweet_text}(parent tweet)"
