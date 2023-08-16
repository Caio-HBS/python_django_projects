from dorin.models import (
    Profile,
    Post,
    Comment,
)
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'comment_text',
            'publication_date_comment',
        ]


class PostSerializer(serializers.ModelSerializer):
    publication_date = serializers.CharField(source='publication_date_post', read_only=True)
    parent_profile = serializers.CharField(source='parent_profile.custom_slug_profile', read_only=True)
    
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = [
            'parent_profile',
            'title',
            'post_text',
            'image',
            'publication_date',
            'post_slug',
            'comments',
        ]


class ProfileBasicSerializer(serializers.ModelSerializer):
    # TODO: Figure out the profile picture.
    class Meta:
        model = Profile
        fields = [
            'user',
            'first_name',
            'full_name',
            'endpoint',
            'endpoint_custom_slug',
            'pk',
        #    'pfp',
        ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    # TODO: Figure out the profile picture.
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = [
            'user',
            'first_name',
            'full_name',
            'endpoint',
            'endpoint_custom_slug',
            'pk',
            'posts',
        #    'pfp',
        ]

