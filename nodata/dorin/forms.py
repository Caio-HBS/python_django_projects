from dorin.models import Post, Profile

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": (
            "Username of password invalid."
        ),
    }


class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Profile
        exclude = ["user", "friends", "pfp"]


class NewPostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    post_text = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Post
        exclude = ["parent_profile", "publication_date_post", "post_slug", "post_text"]
        error_messages = {
            "title": {
                "required": "This field is required.",
                "max_length": "Maximum number characters exceeded."
            },
            "post_text": {
                "required": "This field is required.",
                "max_length": "Maximum number characters exceeded."
            },
    }
        

class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.TextInput())


class PfpForm(forms.Form):
    pfp = forms.ImageField(required=True)

