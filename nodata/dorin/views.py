from datetime import datetime

from dorin.models import Profile

from django.shortcuts import render, redirect
from django.contrib import messages
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
    
    if request.method == "POST":
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
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password != confirm_password:
            messages.error(request, "ERROR: Passwords do not match")
            return render(request, 'dorin/register_page.html')
        
        else:
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            birthday = request.POST['birthday']
            formatted_birthday = datetime.strptime(birthday, "%m/%d/%Y")
            formatted_birthday_to_final = formatted_birthday.strftime("%Y-%m-%d")
            slug = slugify(request.POST['slug'])
        
        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()

        get_user = User.objects.get(username=username)
        profile_info = Profile.objects.create(
            user=get_user,
            birthday=formatted_birthday_to_final,
            pfp="",
            first_name=first_name,
            last_name=last_name,
            custom_slug_profile=slug
        )
        profile_info.save()

    return render(request, 'dorin/register_page.html') 


@login_required(login_url='login_page')
def feed_view(request):
    if request.user.is_authenticated:
        return render(request, 'dorin/feed_page.html')
    else:
        return redirect('login_page')


@login_required(login_url='login_page')
def single_profile_view(request):
    pass


@login_required(login_url='login_page')
def single_post_view(request):
    pass


@login_required(login_url='login_page')
def discover_view(request):
    pass