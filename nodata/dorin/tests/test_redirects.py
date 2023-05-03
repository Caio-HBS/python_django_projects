import pytest

from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.models import User


def test_index_redirect_with_user_should_succed(client, user_logged_in) -> None:
    response = client.get(reverse('index'))
    assert response.status_code == 302
    assert response.url == reverse('feed_page')


def test_index_redirect_no_user_should_succed(client) -> None:
    response = client.get(reverse('index'))
    assert response.status_code == 302
    assert response.url == reverse('login_page')


def test_login_redirect_with_user_should_succed(client, user_logged_in) -> None:
    response = client.get(reverse('login_page'))
    assert response.status_code == 302
    assert response.url == reverse('feed_page')


def test_login_redirect_no_user_should_succed(client) -> None:
    response = client.get(reverse('login_page'))
    assert response.status_code == 200


def test_feed_redirect_with_user_should_succed(client, user_logged_in) -> None:
    response = client.get(reverse('index'))
    assert response.status_code == 302
    assert response.url == reverse('feed_page')


def test_feed_redirect_no_user_should_succed(client) -> None:
    response = client.get(reverse('feed_page'))
    assert response.status_code == 302
    assert response.url == reverse('login_page') + '?next=/dorin/feed/'


def test_register_redirect_create_user_should_succed(client, post_data_for_register) -> None:
    url = reverse('register_page')
    response = client.post(url, data=post_data_for_register)
    assert response.status_code == 302
    assert response.url == reverse('login_page')


def test_register_redirect_user_already_exists_should_succed(client, post_data_for_register) -> None:
    user = User.objects.create_user(
        username='testuser', 
        email='testuser@example.com', 
        password='testuser1234567'
    )
    response = client.post(reverse('register_page'), data=post_data_for_register)
    assert response.status_code == 200
        


def test_register_redirect_logged_in_should_succed(client, user_logged_in) -> None:
    response = client.get(reverse('register_page'))
    assert response.status_code == 302
    assert response.url == reverse('feed_page')