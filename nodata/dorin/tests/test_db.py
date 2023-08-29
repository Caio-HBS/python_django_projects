import pytest

from dorin.models import Post, User
from django.urls import reverse


def test_create_new_user(client, post_data_for_register) -> None:
    """
        Tests the register redirect after creating a new user.

        Args:
            client: standard client provided by pytest-django.
            post_data_for_register: custom fixture that provides a dictionary
            with the required data for registering a new user.
    """
    url = reverse('register_page')
    response = client.post(url, data=post_data_for_register)
    
    assert response.status_code == 302
    assert response.url == reverse('login_page')


def test_create_new_user_username_taken(client, post_data_for_register) -> None:
    """
        Tests the creation of a new user with the username taken.

        Args:
            client: standard client provided by pytest-django.
            post_data_for_register: custom fixture that provides a dictionary
            with the required data for registering a new user.
    """
    user = User.objects.create_user(
        username='testuser', 
        email='testuser@example.com', 
        password='testuser1234567'
    )
    response = client.post(reverse('register_page'), data=post_data_for_register)
    assert response.status_code == 200


def test_create_new_post(client, create_posts_data, user_with_profile) -> None:
    """
        Tests the creation of a new post.

        Args:
            client: standard client provided by pytest-django.
            create_posts_data: custom fixture that provides a dictionary
            with the required data for registering a new post.
            user_with_profile: custom fixture that provides a user AND a profile,
            required for the creation of the post.
    """
    url = reverse('feed_page')
    response = client.post(url, data=create_posts_data, format='multipart')
    assert response.status_code == 302
    assert Post.objects.filter(title='Test Title').exists
    assert response.url == reverse('feed_page')


def test_retrieve_single_post(client, create_posts_data, user_with_profile) -> None:
    """
        Tests the retrieval of a specific post created inside the test. Should
        succeed on both the creation of the post, as well as the correct 
        rendering of the post page.

        Args:
            client: standard client provided by pytest-django.
            create_posts_data: custom fixture that provides a dictionary
            with the required data for registering a new post.
            user_with_profile: custom fixture that provides a user AND a profile,
            required for the creation of the post.
    """
    url_new_post = reverse('feed_page')
    response_for_post_method = client.post(url_new_post, data=create_posts_data, format='multipart')
    
    post_slug = 'test-title'
    post_url = reverse('post_page', kwargs={'post_slug': post_slug})
    response_for_get_method = client.get(post_url)

    assert response_for_post_method.status_code == 302
    assert response_for_get_method.status_code == 200


def test_retrieve_single_profile(client, user_with_profile, post_data_for_register) -> None:
    """
        Tests both the registration of a new profile, as well as the retrieval
        of it. Should succeed on both instances.

        Args:
            client: standard client provided by pytest-django.
            user_with_profile: custom fixture that provides a user AND a profile,
            required for the creation of the post.
            post_data_for_register: custom fixture that provides a dictionary
            with the required data for registering a new user.
    """
    url_for_register = reverse('register_page')
    register_response = client.post(url_for_register, data=post_data_for_register)
    
    profile_slug = 'example_slug'
    url_for_profile = reverse(
        'profile_page', 
        kwargs={'custom_slug_profile': profile_slug}
    )
    profile_response = client.get(url_for_profile)
    assert register_response.status_code == 302
    assert profile_response.status_code == 200
    