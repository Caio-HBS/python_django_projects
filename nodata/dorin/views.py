from datetime import datetime

from dorin.models import (
    Profile, 
    Post, 
    Comment, 
    Likes
)

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Count
from django.utils.text import slugify
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def index_view(request):
    if request.user.is_authenticated:
        return redirect('feed_page')
    else:
        return redirect('login_page')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed_page')
    
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "ERROR: Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('feed_page')
        else:
            messages.error(request, "ERROR: Username OR password wrong")

    return render(request, 'dorin/login_page.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login_page')
    else:
        return redirect('login_page')
    

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed_page')
    elif request.method == "POST":
        username = request.POST['username']
        # Tests to see if the username is already in use in the db.
        try:
            get_user = User.objects.get(username=username)
        except User.DoesNotExist:
            password = request.POST['password']
            confirm_password = request.POST['confirm-password']
            # Tests to see if the passwords match.
            if password != confirm_password:
                messages.error(request, "ERROR: Passwords do not match")
                return render(request, 'dorin/register_page.html')
            # Creates the new user based on the passed-on data.
            else:
                email = request.POST['email']
                first_name = request.POST['first-name']
                last_name = request.POST['last-name']
                birthday = request.POST['birthday']
                pfp = request.FILES['profile-picture']
                formatted_birthday = datetime.strptime(birthday, "%m/%d/%Y")
                formatted_birthday_to_final = formatted_birthday.strftime("%Y-%m-%d")
                slug = slugify(request.POST['slug'])
        
                new_user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                new_user.save()
                # Tests to see if the user was created. If it was, creates the 
                # profile object.
                try:
                    get_new_user = User.objects.get(username=username)
                except User.DoesNotExist:
                    messages.error(request, "ERROR: error while retrieving user")
                    return render(request, 'dorin/register_page.html')
                else:
                    profile_info = Profile.objects.create(
                    user=get_new_user,
                    birthday=formatted_birthday_to_final,
                    pfp=pfp,
                    first_name=first_name,
                    last_name=last_name,
                    custom_slug_profile=slug
                    )
                    profile_info.save()
                    print("DB: New user and profile created successfully")
                    return redirect('login_page')
        else:
            messages.error(request, "ERROR: Username already in use")
            return render(request, 'dorin/register_page.html')
        
    return render(request, 'dorin/register_page.html') 


@login_required(login_url='login_page')
def feed_view(request):
    # Retrieves the user from the request, so that the query can be made.
    user = request.user
    profile = Profile.objects.get(user=user)
    friends = profile.friends.all()
    # Uses the Q class for a more advanced query.
    q = Q(parent_profile__in=friends) | Q(parent_profile=profile)
    posts = Post.objects.filter(q).order_by("-publication_date_post")
    # Appends the retrieved data in a list so that it can be passed as a context
    #  dict.
    context_list = []
    for post in posts:
        comments = Comment.objects.filter(parent_post=post)
        likes = Likes.objects.filter(parent_post=post)
        context_list.append({
            'post': post,
            'comments': comments,
            'likes': likes,
        })
    return render(request, 'dorin/feed_page.html', {'posts': context_list})
    

@login_required(login_url='login_page')
def new_post_view(request):
    if request.method == "POST":
        # Retrieves the user so that the new post can be saved,
        user = request.user
        try:
            get_user = User.objects.get(username=user)
        except:
            messages.error(
                'There has been an error retrieving your data, we are sorry :('
            )
        # Uses the data to create the object for the post and saves it, 
        # redirecting the user afterwards.
        get_user_profile = get_user.profile
        title = request.POST['title'][:50].rstrip()
        post_text = request.POST['post-text'].rstrip()
        
        try:
            image = request.FILES['post-picture']
        except:
            image = ""

        new_post = Post.objects.create(
            parent_profile=get_user_profile, title=title, 
            post_text=post_text, image=image, post_slug=slugify(title)
        )
        new_post.save()
        return redirect('feed_page')

    return render(request, 'dorin/new_post_page.html')


@login_required(login_url='login_page')
def single_profile_view(request, custom_slug_profile):
    try:
        profile = Profile.objects.filter(custom_slug_profile=custom_slug_profile)
    except:
        messages.error("We are sorry, but there's been an error")
    else:
        
        return render(request, 'dorin/profile_page.html', {
            "profile": profile
        })

    return render(request, 'dorin/profile_page.html')


@login_required(login_url='login_page')
def single_post_view(request, post_slug):
    try:
        post = Post.objects.filter(post_slug=post_slug)
    except:
        messages.error("We are sorry, but there's been an error")
    else:
        
        return render(request, 'dorin/post_page.html', {
            "post": post
        })
    
    return render(request, 'dorin/post_page.html')


@login_required(login_url='login_page')
def discover_view(request):
    current_user = request.user
    current_profile = current_user.profile
    max_posts = 10
    # A quick way to make a query with the desired maximum number of posts.
    posts = Post.objects.exclude(parent_profile=current_profile).annotate(num_likes=Count('likes')).order_by('?')[:max_posts]
    
    return render(request, 'dorin/discover_page.html', {
        'posts': posts
    })
    