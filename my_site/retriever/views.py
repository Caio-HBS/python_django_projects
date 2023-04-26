from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode

from .models import (
    YouTubeVideo,
    YouTubeVideoKeyword, 
    Tweet,
    TweetKeyword, 
    InstagramPost, 
    InstagramPostImage
)
from .forms import SearchForm

from colorama import Fore
from dotenv import load_dotenv

import requests
import json
import os

load_dotenv()

def api_fetcher_twitter(user, keyword=False, debug=False):
    """
        Makes the API call to the Twitter server and stores the data in the db.

        Args:
            user: the username of the profile (has to be the exact same as the 
            twitter handle).
            keyword: a keyword that helps narrow down the search, might be empty.
            debug: a boolean to tell the function to print the API response.
    """
    bearer_token = os.environ.get("BEARER_TOKEN_TWITER")

    # Makes the request so that it can fetch the tweets.
    if keyword:
        url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}(from:{user})&tweet.fields=text,created_at&media.fields=preview_image_url,url&user.fields=profile_image_url&expansions=attachments.media_keys,author_id"
        keyword_value = keyword
    else:
        url = f"https://api.twitter.com/2/tweets/search/recent?query=(from:{user})&tweet.fields=text,created_at&media.fields=preview_image_url,url&user.fields=profile_image_url&expansions=attachments.media_keys,author_id"
        keyword_value = ""

    headers = {"Authorization": f"Bearer {bearer_token}"}
    response_data = requests.get(url, headers=headers)

    if debug:
        print("\n\n", response_data.status_code)
        print("\n\n", json.dumps(response_data.json(), indent=4))

    if response_data.status_code == 200:
        received = response_data.json()
    else:
        return "Error fetching the requested data"
    # Unpacks the .json into a list of dictionaries.
    tweets = []
    for tweet in received['data']:
        tweet_dict = {
            'user': received['includes']['users'][0]['username'],
            'display_name': received['includes']['users'][0]['name'],
            'profile_image': received['includes']['users'][0]['profile_image_url'][:-11] + ".jpg",
            'tweet_text': tweet['text'][:280],
            'url': f'https://twitter.com/{received["includes"]["users"][0]["username"]}/status/{tweet["id"]}',
            'post_date': tweet['created_at'][:10],
            'image': ''
        }
        # Checks to see if the tweet has images/videos (appends just a thumbnail
        # in the second case).
        if 'attachments' in tweet and 'media_keys' in tweet['attachments']:
            media_key = tweet['attachments']['media_keys']
            for media in received['includes']['media']:
                if media_key[0] == media['media_key']:
                    if media['type'] == 'video' and 'preview_image_url' in media:
                        tweet_dict['image'] = media['preview_image_url']
                    elif media['type'] == 'photo':
                        tweet_dict['image'] = media['url']
                    break
        tweets.append(tweet_dict)

    # Loops through the list checking to see if the tweets are in the db, if not,
    # stores them, and if they are but under a different keyword, create the 
    # object for the new one.
    for tweet in tweets:
        if Tweet.objects.filter(url=tweet['url']).exists():
            found_tweet = Tweet.objects.get(url=tweet['url'])
            if keyword_value != "":
                print(Fore.CYAN + " Twitter API: found tweet in db, updating it")
                new_tweet_keyword = TweetKeyword.objects.create(
                    tweet=found_tweet,
                    keyword=keyword_value
                )
                new_tweet_keyword.save()
            else:
                print(Fore.CYAN + " Twitter API: found tweet in db")
        else:
            print(Fore.CYAN + "Twitter API: tweet not found, creating new object")
            new_tweet = Tweet.objects.create(
                user=tweet['user'],
                display_name=tweet['display_name'],
                profile_image=tweet['profile_image'],
                tweet_text=tweet['tweet_text'],
                image=tweet['image'],
                url=tweet['url'],
                post_date=tweet['post_date'],
            )
            new_tweet.save()
            if keyword_value != "":
                new_tweet_keyword = TweetKeyword.objects.create(
                    tweet=new_tweet,
                    keyword=keyword_value
                )
                new_tweet_keyword.save()


def api_fetcher_youtube(user, keyword=False, debug=False):
    """
        Makes the API call to the YouTube server and stores the data in the db.

        Args:
            user: the username of the profile (has to be the exact same as the 
            channel).
            keyword: a keyword that helps narrow down the search, might be empty.
            debug: a boolean to tell the function to print the API response.
    """
    api_key = os.environ.get("API_KEY_YOUTUBE")

    # Fetches the correct channel ID for the desired username, as well as the 
    # profile picture for that.
    url_channel_id = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={user}&type=channel&key={api_key}"

    response_channel_id = requests.get(url_channel_id)

    if debug:
        print("Debug response for API call channel id")
        print("\n\n", response_channel_id.status_code)
        print("\n\n", json.dumps(response_channel_id.json(), indent=4))

    if response_channel_id.status_code == 200:
        received_channel_id = response_channel_id.json()

    channel_id = received_channel_id['items'][0]['id']['channelId']
    pfp = received_channel_id["items"][0]["snippet"]["thumbnails"]["high"]["url"]

    if not keyword:
        keyword = ""

    # Makes the API call to retrieve the actual videos.
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=20&q={keyword}"
    response = requests.get(url)

    if response.status_code == 200:
        received = response.json()

    if debug:
        print("Debug response for actual API call")
        print("\n\n", response.status_code)
        print("\n\n", json.dumps(response.json(), indent=4))

    # Unpacks the .json into a list of dictionaries.
    videos = []
    for item in received['items']:
        if item['id']['kind'] == 'youtube#video':
            video = {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'upload_date': item['snippet']['publishedAt'][:10],
                'description_excerpt': item['snippet']['description'],
                'channel_name': item['snippet']['channelTitle'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'profile_image': pfp,
            }
            videos.append(video)
   
    # Loops through the list checking to see if the videos are in the db, if not,
    # stores them, and if they are but under a different keyword, create the 
    # object for the new one.
    for single_video in videos:
        if YouTubeVideo.objects.filter(url=single_video['url']).exists():
            found_video = YouTubeVideo.objects.get(url=single_video['url'])
            if keyword != "":
                print(Fore.CYAN + " YouTube API: found video in db, updating it")
                new_video_keyword = YouTubeVideoKeyword.objects.create(
                    yt_video=found_video,
                    keyword=keyword
                )
                new_video_keyword.save()
            else:
                print(Fore.CYAN + " YouTube API: found video in db")
        else:
            print(Fore.RED + "YouTube API: video not found, creating new object")
            new_video = YouTubeVideo.objects.create(
                title=single_video['title'],
                url=single_video['url'],
                upload_date=single_video['upload_date'],
                description_excerpt=single_video['description_excerpt'],
                channel_name=single_video['channel_name'],
                thumbnail=single_video['thumbnail'],
                profile_image=single_video['profile_image'],
            )
            new_video.save()
            if keyword != "":
                new_video_keyword = YouTubeVideoKeyword.objects.create(
                    yt_video=new_video,
                    keyword=keyword
                )
                new_video_keyword.save()
            

def api_fetcher_instagram(user, debug=False):
    """
        Makes the API call to the Instagram server and stores the data in the db.

        Args:
            user: the username of the profile (has to be the exact same as the 
            handle).
            debug: a boolean to tell the function to print the API response.
    """
    ig_access_token = os.getenv("LONG_LIVED_ACCESS_TOKEN_IG")
    ig_user_id = os.getenv("USER_ID_IG")

    # Handles the API request.
    url = "https://graph.facebook.com/v16.0/" + ig_user_id + "?fields=business_discovery.username(" + user + "){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media{id,caption,like_count,comments_count,timestamp,username,media_product_type,media_type,owner,permalink,media_url,children{media_url}}}&access_token=" + ig_access_token

    response = requests.get(url)

    if debug:
        print("\n\n", response.status_code)
        print("\n\n", json.dumps(response.json(), indent=4))

    if response.status_code == 200:
        received = response.json()

        # Unpacks the .json into a list of dictionaries.
        ig_posts = []
        for post in received["business_discovery"]["media"]["data"]:
            ig_username = received["business_discovery"]["username"]
            ig_display_name = received["business_discovery"]["name"]
            caption = post.get("caption", "")
            comments_count = post.get("comments_count", 0)
            likes_count = post.get("like_count", 0)
            post_time = post.get("timestamp", "")
            profile_picture = received["business_discovery"]["profile_picture_url"]
            post_url = post.get("permalink", "")
            media_type = post.get("media_type", "")
            media_url = post.get("media_url", "")

            post_dict = {
                "ig_username": ig_username,
                "ig_display_name": ig_display_name,
                "caption": caption,
                "comments_count": comments_count,
                "likes_count": likes_count,
                "post_time": post_time[:10],
                "media_type": media_type,
                "profile_picture": profile_picture,
                "post_url": post_url,
                "media_url": media_url
            }
            if post['media_type'] == 'CAROUSEL_ALBUM':
                carousel_urls = []
                for child in post['children']['data']:
                    child_media_url = child.get('media_url')
                    if child_media_url is not None:
                        carousel_urls.append(child_media_url)
                        post_dict['media_url'] = carousel_urls

            ig_posts.append(post_dict)
        # Loops through the list checking to see if the IG posts are in the db, if 
        # not, stores them.
        for post in ig_posts:
            if InstagramPost.objects.filter(post_url=post["post_url"]).exists():
                print(Fore.MAGENTA + " Instagram API: found post in db")
                pass
            else:
                if post['media_type'] != "VIDEO":
                    print(Fore.MAGENTA + "Instagram API: post not found, creating new object")
                    new_ig_post = InstagramPost.objects.create(
                        ig_username=post['ig_username'],
                        ig_display_name=post['ig_display_name'],
                        caption=post['caption'],
                        comments_count=post['comments_count'],
                        likes_count=post['likes_count'],
                        post_time=post['post_time'],
                        profile_picture=post['profile_picture'],
                        post_url=post['post_url'],
                        media_type=post['media_type'],
                    )
                    new_ig_post.save()
                    if post['media_type'] == "CAROUSEL_ALBUM":
                        for image in post['media_url']:
                            new_carousel = InstagramPostImage.objects.create(
                                instagram_post=new_ig_post,
                                image_url=image
                            )
                            new_carousel.save()
                    else:
                        new_media_url = InstagramPostImage.objects.create(
                                instagram_post=new_ig_post,
                                image_url=post['media_url']
                        )
                        new_media_url.save()


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            platform = form.cleaned_data['platform']
            user = form.cleaned_data['username']
            keyword = form.cleaned_data['keyword']
        
            if platform == "Twitter":
                url = reverse("tweets_page") + "?" + urlencode({
                    "user": user, 
                    "keyword": keyword
                })
                return redirect(url)
            elif platform == "YouTube":
                url = reverse("yt_videos_page") + "?" + urlencode({
                    "user": user, 
                    "keyword": keyword
                })
                return redirect(url)
            elif platform == "Instagram":
                url = reverse("insta_posts_page") + "?" + urlencode({
                    "user": user, 
                })
                return redirect(url)
            elif platform == "Facebook":
                return redirect("fb_posts_page", user=user, keyword=keyword)
    else:
        form = SearchForm()
    return render(request, 'retriever/index.html', {'form': form})    


def twitter_view(request):
    user = str(request.GET.get('user'))
    keyword = str(request.GET.get('keyword', False))

    if keyword:
        if TweetKeyword.objects.filter(keyword=keyword).exists():
            tweets_keywords = TweetKeyword.objects.filter(keyword=keyword)
            if Tweet.objects.filter(user=user, tweetkeyword__in=tweets_keywords):
                print(Fore.GREEN + "SERVER: reaching database only (Twitter)")
                returned_tweets = Tweet.objects.filter(
                    user=user, 
                    tweetkeyword__in=tweets_keywords).order_by("-post_date")
                return render(request, "retriever/tweets.html", {
                    "tweets": returned_tweets
                })
        else:
            print(Fore.GREEN + "SERVER: reaching Twitter API with user and keyword")
            api_fetcher_twitter(user, keyword)
            tweets_keywords = TweetKeyword.objects.filter(keyword=keyword)
            returned_tweets = Tweet.objects.filter(
                    user=user, 
                    tweetkeyword__in=tweets_keywords).order_by("-post_date")
            return render(request, "retriever/tweets.html", {
                "tweets": returned_tweets
            })

    else:
        print(Fore.GREEN + "SERVER: reaching Twitter API with user only")
        api_fetcher_twitter(user)
        returned_tweets = Tweet.objects.filter(
            user__icontains=user).order_by("-post_date")[:15]
        return render(request, "retriever/tweets.html", {
            "tweets": returned_tweets
        })


def youtube_view(request):
    user = str(request.GET.get('user'))
    keyword = str(request.GET.get('keyword', False))
    
    if keyword:
        if YouTubeVideoKeyword.objects.filter(keyword=keyword).exists():
            video_keywords = YouTubeVideoKeyword.objects.filter(keyword=keyword)
            if YouTubeVideo.objects.filter(channel_name=user, youtubevideokeyword__in=video_keywords):
                print(Fore.GREEN + "SERVER: reaching database only (YouTube)")
                returned_videos = YouTubeVideo.objects.filter(
                    channel_name=user, 
                    youtubevideokeyword__in=video_keywords).order_by("-upload_date")
                return render(request, "retriever/yt-videos.html", {
                    "videos": returned_videos
                })
        else:
            print(Fore.GREEN + "SERVER: reaching YouTube API with user and keyword")
            api_fetcher_youtube(user, keyword)
            video_keywords = YouTubeVideoKeyword.objects.filter(keyword=keyword)
            returned_videos = YouTubeVideo.objects.filter(
                    channel_name=user, 
                    youtubevideokeyword__in=video_keywords).order_by("-upload_date")
            return render(request, "retriever/yt-videos.html", {
                "videos": returned_videos
            })
    else:
        print(Fore.GREEN + "SERVER: reaching YouTube API with user only")
        api_fetcher_youtube(user)
        returned_videos = YouTubeVideo.objects.filter(
            channel_name__icontains=user).order_by("-upload_date")
        return render(request, "retriever/yt-videos.html", {
            "videos": returned_videos
        })
    

def instagram_view(request):
    user = str(request.GET.get('user'))

    print(Fore.GREEN + "SERVER: reaching Instagram API")
    api_fetcher_instagram(user)
    returned_posts = InstagramPost.objects.filter(
        ig_username__icontains=user).order_by("-post_time")
    return render(request, "retriever/ig_posts.html", {
        "posts": returned_posts
    })
