from django.contrib import admin
from .models import (
    YouTubeVideo,
    YouTubeVideoKeyword, 
    Tweet, 
    TweetKeyword,
    InstagramPost, 
    InstagramPostImage
)

admin.site.register(Tweet)
admin.site.register(TweetKeyword)
admin.site.register(YouTubeVideo)
admin.site.register(YouTubeVideoKeyword)
admin.site.register(InstagramPost)
admin.site.register(InstagramPostImage)
