from django.utils.dateformat import format

from dorin.models import (
    Profile, 
    Post, 
    Comment, 
)

from dorin.forms import (
    LoginForm, 
    NewPostForm, 
    RegisterForm, 
    CommentForm, 
    PfpForm,
    FriendToggleForm,
)

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.text import slugify
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index_view(request):
    """
        Redirects users based on authentication status.

        This view checks if the user is authenticated. If authenticated, it 
        redirects to the feed page ('feed_page'). Otherwise, it redirects to the 
        login page ('login_page').

        URL Call: /
    """
    if request.user.is_authenticated:
        return redirect('feed_page')
    else:
        return redirect('login_page')


def login_view(request):
    """
        View for loggin in users.

        If the user is already logged in, redirects to feed page, otherwise
        validates the post request for loggin them in.
    
        URL Call: dorin/login/
    """
    if request.user.is_authenticated:
        return redirect('feed_page')
    
    elif request.method == "POST":
        auth_form = LoginForm(data=request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            login(request, user)
            return redirect('feed_page')
        else:
            return render(request, 'dorin/login_page.html', {"form": auth_form})
    else:
        auth_form = LoginForm()
        return render(request, 'dorin/login_page.html', {"form": auth_form})


def logout_view(request):
    """
        Logs the user out uppon hitting the URL based on login status.

        If the user is logged in, logs out. Otherwise, simply redirects them to
        the login page.

        URL Call: dorin/logout/
    """
    
    if request.user.is_authenticated:
        logout(request)
        return redirect('login_page')
    else:
        return redirect('login_page')
    
    
class RegisterView(View):
    """
        Class-based view for registering new users.

        If the user is already logged in, redirects them to the feed page, 
        otherwise validates the post request for register as new users.

        URL Call: dorin/register/
    """

    def get(self, request):
        """
            Handles the GET method to simply render the register page with the 
            form.
        """
        if request.user.is_authenticated:
            return redirect('login_page')
        else:
            context = {
                "form": RegisterForm()
            }
            return render(request, 'dorin/register_page.html', context)

    def post(self, request):
        """
            Handles the POST method registration.
        """
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            confirm_password = register_form.cleaned_data['confirm_password']
            custom_slug_profile = register_form.cleaned_data['custom_slug_profile']
            
            # Password check
            if password != confirm_password:
                register_form.add_error('confirm_password', 'Passwords do not match.')
                return render(request, 'dorin/register_page.html', {'form': register_form})
            # Username check.
            if User.objects.filter(username=username).exists():
                register_form.add_error('username', 'This username is already taken.')
                return render(request, 'dorin/register_page.html', {'form': register_form})
            # Slug check.
            if Profile.objects.filter(custom_slug_profile=custom_slug_profile).exists():
                register_form.add_error('custom_slug_profile', 'This custom slug is already taken.')
                return render(request, 'dorin/register_page.html', {'form': register_form})
            
            new_user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password
            )
            Profile.objects.create(
                user=new_user, 
                birthday=register_form.cleaned_data['birthday'],
                first_name=register_form.cleaned_data['first_name'],
                last_name=register_form.cleaned_data['last_name'],
                custom_slug_profile=custom_slug_profile, 
            )
            
            return redirect('login_page')

        context = {
            "form": register_form
        }
        return render(request, 'dorin/register_page.html', context)


class FeedView(View):
    """
        Feed view for seeing posts by the user and their friends (locked to
        logged in users).

        URL Call: dorin/feed/
    """
    def get(self, request):
        """
            Handles the GET method by querying the posts objects based on the 
            user and their friends, passes it to the html template.
        """
        user = request.user
        profile = Profile.objects.get(user=user)
        friends = profile.friends.all()
        new_post_form = NewPostForm()
        
        q = Q(parent_profile__in=friends) | Q(parent_profile=profile)
        posts = Post.objects.filter(q).order_by("-publication_date_post")
        context_list_for_posts = []
        for post in posts:
            context_list_for_posts.append({
                'post': post,
                'slug': post.post_slug,
                'profile': post.parent_profile,
            })

        context = {
            'posts': context_list_for_posts,
            'form': new_post_form,
            'profile': profile,
        }
        return render(request, 'dorin/feed_page.html', context)
    
    def post(self, request):
        """
            Handles the POST method by validating the form and making it a new
            post if valid.
        """
        post_form = NewPostForm(request.POST, request.FILES)
        user = request.user
        retrieved_user = get_object_or_404(User, username=user)

        if post_form.is_valid():
            get_user_profile = retrieved_user.profile
            title = post_form.cleaned_data['title']
            post_text = post_form.cleaned_data['post_text']
        
            try:
                image = post_form.cleaned_data['image']
            except:
                image = ""

            new_post = Post.objects.create(
                parent_profile=get_user_profile, title=title, 
                post_text=post_text, image=image, post_slug=slugify(title)
            )
            new_post.save()
            return redirect('feed_page')
        else:
            return render(request, 'dorin/feed_page.html', {'form': post_form})
decorated_feed_view = login_required(login_url='login_page')(FeedView.as_view())


@login_required(login_url='login_page')
def single_profile_view(request, custom_slug_profile):
    """
        View for displaying specific profiles.
        
        Queries the db for a profile based on the custom_slug_profile passed in
        through the url.

        URL Call: profile/<slug:custom_slug_profile>/

        Params:
            custom_slug_profile: slug passed in the url reflecting an object on 
            the db.
    """
    retrieved_profile = get_object_or_404(Profile, custom_slug_profile=custom_slug_profile)
    logged_in_profile = request.user.profile
    posts = retrieved_profile.posts.all()
    
    if request.method == "POST":
        change_pfp_form = PfpForm(request.POST, request.FILES)
        add_friend_form = FriendToggleForm(request.POST)
        
        if change_pfp_form.is_valid():
            new_pfp = change_pfp_form.cleaned_data['pfp']
            retrieved_profile.pfp = new_pfp
            retrieved_profile.save()
            return redirect(
                "profile_page", custom_slug_profile=custom_slug_profile
            )
        
        elif add_friend_form.is_valid():
            action = add_friend_form.cleaned_data['action']
            if action == 'add_friend':
                logged_in_profile.friends.add(retrieved_profile)
            elif action == 'unfriend':
                logged_in_profile.friends.remove(retrieved_profile)
            return redirect(
                "profile_page", custom_slug_profile=custom_slug_profile
            )

    else:
        change_pfp_form = PfpForm()
        add_friend_form = FriendToggleForm()
        
    return render(request, 'dorin/profile_page.html', {
        "profile": retrieved_profile,
        "posts": posts,
        "form": change_pfp_form,
        "friend_form": add_friend_form,
        'custom_slug_profile': custom_slug_profile
    })


@login_required(login_url='login_page')
def single_post_view(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)
    comments_on_post = post.comments.all
    time_of_post = post.publication_date_post
    formatted_time = format(time_of_post, "F j, Y H:i")
    comment_form = CommentForm(request.POST)
    context = {
        "slug": post_slug,
        "comments": comments_on_post,
        "post": post,
        "form": comment_form,
        "time": formatted_time,
    }
    if request.method == "POST":
        if comment_form.is_valid():   
            user = request.user
            print(request.user)
            comment_text = comment_form.cleaned_data['comment_text']
            Comment.objects.create(
                user=user, 
                parent_post=post, 
                comment_text=comment_text, 
            )
            return render(request, 'dorin/post_page.html', context)

    return render(request, 'dorin/post_page.html', context)


@login_required(login_url='login_page')
def discover_view(request):
    """
        Discover view for retrieving random posts (locked to logged in users).

        Makes the query for random posts excluding those made by the user.

        URL Call: dorin/discover/
    """
    current_user = request.user
    current_profile = current_user.profile
    max_posts = 10
    
    posts = Post.objects.exclude(parent_profile=current_profile).order_by('?')[:max_posts]
    
    return render(request, 'dorin/discover_page.html', {
        'posts': posts
    })


def about_us_view(request):
    return render(request, 'dorin/about_us.html')
