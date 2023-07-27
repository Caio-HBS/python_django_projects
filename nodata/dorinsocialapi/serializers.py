from dorin.models import (
    Profile,
    Post,
)
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
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


class PostSerializer(serializers.ModelSerializer):
    publication_date = serializers.CharField(source='publication_date_post')
    class Meta:
        model = Post
        fields = [
            'title',
            'post_text',
            'image',
            'publication_date',
            'post_slug',
        ]