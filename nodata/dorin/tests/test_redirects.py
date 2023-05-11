import pytest

from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.models import User


def test_index_redirect_with_user(client, user_logged_in) -> None:
    """
        Tests the redirect of the index page with a user logged in. Should send 
        the client to the feed page.

        Args:
            client: standard client provided by pytest-django.
            user_logged_in: custom fixture to provide a logged in user for the 
            client.
    """
    response = client.get(reverse('index'))
    assert response.status_code == 302
    assert response.url == reverse('feed_page')


def test_index_redirect_no_user(client) -> None:
    """
        Tests the redirect of the index page with no user logged in. Should send 
        the client to the login page.

        Args:
            client: standard client provided by pytest-django.
    """    
    response = client.get(reverse('index'))
    assert response.status_code == 302
    assert response.url == reverse('login_page')


def test_login_redirect_with_user(client, user_logged_in) -> None:
    """
        Tests the redirect of the login page with a user logged in. Should send 
        the client to the feed page.

        Args:
            client: standard client provided by pytest-django.
            user_logged_in: custom fixture to provide a logged in user for the 
            client.
    """
    response = client.get(reverse('login_page'))
    assert response.status_code == 302
    assert response.url == reverse('feed_page')


def test_login_redirect_no_user(client) -> None:
    """
        Tests the redirect of the login page with no user logged in. Should not  
        redirect the client to any other page.

        Args:
            client: standard client provided by pytest-django.
    """
    response = client.get(reverse('login_page'))
    assert response.status_code == 200


def test_feed_redirect_with_user(client, user_logged_in) -> None:
    """
        Tests the redirect of the feed page with a user logged in. Should allow 
        the client to view the page without the redirecting.

        Args:
            client: standard client provided by pytest-django.
            user_logged_in: custom fixture to provide a logged in user for the 
            client.

    """
    response = client.get(reverse('index'))
    assert response.status_code == 302
    assert response.url == reverse('feed_page')


def test_feed_redirect_no_user(client) -> None:
    """
        Tests the redirect of the feed page with no user logged in. Should send
        the client back to the login page with the appended feed as the next 
        redirect url.

        Args:
            client: standard client provided by pytest-django.
    """
    response = client.get(reverse('feed_page'))
    assert response.status_code == 302
    assert response.url == reverse('login_page') + '?next=/dorin/feed/'
        

def test_register_redirect_logged_in(client, user_logged_in) -> None:
    """
        Tests the register redirect with a user already logged in.

        Args:
            client: standard client provided by pytest-django.
            user_logged_in: custom fixture to provide a logged in user for the 
            client.
    """
    response = client.get(reverse('register_page'))
    assert response.status_code == 302
    assert response.url == reverse('feed_page')
