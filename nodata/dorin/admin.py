from django.contrib import admin
from .models import Post, Comment, Profile


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"post_slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
