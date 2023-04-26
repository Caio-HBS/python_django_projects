import os
import json
import pytest

from django.urls import reverse
from django.test import Client
from retriever.models import (
    YouTubeVideo,
    Tweet,
)
from my_site.settings import BASE_DIR 
from django.utils.http import urlencode


test_data_path = os.path.join(
    BASE_DIR, r"retriever/tests/received.json"
)

with open(test_data_path, "r") as base:
    base_json = json.load(base)

pytestmark = pytest.mark.django_db

@pytest.mark.twitter
def test_write_twitter_db_no_image_should_succed(client) -> None:
    test_tweet_no_image = Tweet.objects.create(
        user=base_json['Twitter']['includes']['users'][0]['username'],
        display_name=base_json['Twitter']['includes']['users'][0]['name'],
        profile_image=base_json['Twitter']['includes']['users'][0]['profile_image_url'],
        tweet_text=base_json['Twitter']['data'][1]['text'],
        image="",
        url=f"https://twitter.com/{base_json['Twitter']['includes']['users'][0]['username']}/status/{base_json['Twitter']['data'][1]['id']}",
        post_date=base_json['Twitter']['data'][1]['created_at'][:10]
    )
    test_tweet_no_image.save()

    assert Tweet.objects.filter(
        user="LEGO_Group",
        display_name="LEGO",
        profile_image="https://pbs.twimg.com/profile_images/1198949412237709313/kXmJNLLH_normal.jpg",
        tweet_text="@Icecreamlord31 https://t.co/LRXuwsgEtf",
        image="",
        url="https://twitter.com/LEGO_Group/status/1650885170524725248",
        post_date="2023-04-25"
    ).exists()


@pytest.mark.twitter
def test_write_twitter_db_with_image_should_succed(client) -> None:
    if base_json['Twitter']['includes']['media'][0]['media_key'] == base_json['Twitter']['data'][0]['attachments']['media_keys'][0]:
        img_second_tweet = base_json['Twitter']['includes']['media'][0]['url']

    test_tweet_with_image = Tweet.objects.create(
        user=base_json['Twitter']['includes']['users'][0]['username'],
        display_name=base_json['Twitter']['includes']['users'][0]['name'],
        profile_image=base_json['Twitter']['includes']['users'][0]['profile_image_url'],
        tweet_text=base_json['Twitter']['data'][0]['text'],
        image=img_second_tweet,
        url=f"https://twitter.com/{base_json['Twitter']['includes']['users'][0]['username']}/status/{base_json['Twitter']['data'][0]['id']}",
        post_date=base_json['Twitter']['data'][0]['created_at'][:10]
    )
    test_tweet_with_image.save()

    assert Tweet.objects.filter(
        user="LEGO_Group",
        display_name="LEGO",
        profile_image="https://pbs.twimg.com/profile_images/1198949412237709313/kXmJNLLH_normal.jpg",
        tweet_text="@d4mnbrothatsmad We'll do our best so you can get back to building! 📦",
        image="https://pbs.twimg.com/ext_tw_video_thumb/1650907567873314816/pu/img/C3m0muSQAvD4rQHn.jpg",
        url="https://twitter.com/LEGO_Group/status/1650927131709284363",
        post_date="2023-04-25"
    ).exists()


@pytest.mark.youtube
def test_write_youtube_db_should_succed(client) -> None:
    new_test_video = YouTubeVideo.objects.create(
        title=base_json['YouTube']['items'][0]['snippet']['title'],
        url=f"https://www.youtube.com/watch?v={base_json['YouTube']['items'][0]['id']['videoId']}",
        upload_date=base_json['YouTube']['items'][0]['snippet']['publishedAt'][:10],
        description_excerpt=base_json['YouTube']['items'][0]['snippet']['description'],
        channel_name=base_json['YouTube']['items'][0]['snippet']['channelTitle'],
        thumbnail=base_json['YouTube']['items'][0]['snippet']['thumbnails']['high']['url'],
        profile_image=""
    )
    new_test_video.save()

    assert YouTubeVideo.objects.filter(
        title="Destiny 2: Lightfall - The Game Awards Trailer | PS5 &amp; PS4 Games",
        url="https://www.youtube.com/watch?v=LYJMdxHTPiI",
        upload_date="2022-12-09",
        description_excerpt="https://www.playstation.com/en-us/games/destiny-2/ Our end begins. Shattered glass glints in the starlight. Soldiers of the Shadow ...",
        channel_name="PlayStation",
        thumbnail="https://i.ytimg.com/vi/LYJMdxHTPiI/hqdefault.jpg",
        profile_image=""
    ).exists()


@pytest.mark.view
def test_index_view_should_succed(client) -> None:
    client = Client()
    url = reverse("index_page")
    response = client.get(url)

    assert response.status_code == 200

@pytest.mark.view
@pytest.mark.twitter
def test_twitter_view_should_succed(client) -> None:
    client = Client()
    url = reverse("tweets_page") + "?" + urlencode({
                    "user": "PlayStation", 
                    "keyword": ""
                })
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.view
@pytest.mark.youtube
def test_youtube_view_should_succed(client) -> None:
    client = Client()
    url = reverse("yt_videos_page")
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.view
@pytest.mark.instagram
def test_instagram_view_should_succed(client) -> None:
    client = Client()
    url = reverse("insta_posts_page")
    response = client.get(url)

    assert response.status_code == 200