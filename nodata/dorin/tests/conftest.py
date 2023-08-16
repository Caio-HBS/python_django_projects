import os
import pytest

from dorin.models import Profile

from django.urls import reverse
from django.contrib.auth.models import User

from nodata.settings import BASE_DIR


image_file_path = os.path.join(
    BASE_DIR, r"dorin/tests/test_image.jpg"
)

@pytest.fixture
def user_logged_in(client, db):
    """
        A fixture to make sure the redirects will work as intended with a logged 
        in user.

        Args:
            client: uses the Pytest-Django built-in client.
            db: uses the Pytest-Django built-in db.
    """
    user = User.objects.create_user(
        username='example', email='email@holder.com', password='1325Gy:*'
    )
    client.force_login(user)
    return user


@pytest.fixture
def user_with_profile(client, db):
    """
        Fixture to provide both a user and a profile.

        Args:
            client: uses the Pytest-Django built-in client.
            db: uses the Pytest-Django built-in db.
    """
    user = User.objects.create_user(
        username='example', email='email@holder.com', password='1325Gy:*'
    )
    get_user = User.objects.get(username='example')
    new_profile = Profile.objects.create(
                    user=get_user,
                    birthday='2001-01-01',
                    pfp="",
                    first_name='John',
                    last_name='Doe',
                    custom_slug_profile='example_slug'
                    )
    new_profile.save()
    client.force_login(user)
    return user


@pytest.fixture
def post_data_for_register(client, db):
    """
        Fixture to provide data to POST method in the register page.

        Args:
            client: uses the Pytest-Django built-in client.
            db: uses the Pytest-Django built-in db.
    """
    image_file = open(image_file_path, 'rb')
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'first-name': 'John',
        'last-name': 'Doe',
        'birthday': '01/01/1990',
        'slug': 'testuser1234567',
        'password': 'testpassword123',
        'confirm-password': 'testpassword123',
        'profile-picture': ""
    }


@pytest.fixture
def create_posts_data(client, db):
    """
        Fixture to provide data for test involving new posts.

        Args:
            client: uses the Pytest-Django built-in client.
            db: uses the Pytest-Django built-in db.
    """
    return {
        'title': 'Test Title',
        'post_text': 'This is a test for the post text',
    }


@pytest.fixture
def normal_user_token_retrieve(client, user_with_profile):
    url = reverse('api_get_auth_token')
    data = {'username': 'example', 'password': '1325Gy:*'}
    response_data = client.post(url, data=data)
    response_data_json = response_data.json()
    token = response_data_json['token']
    return token


@pytest.fixture
def staff_user_token_retrieve(client, db):
    username = 'admin'
    password = 'adminpassword'
    User.objects.create_user(
        username=username,
        email='emain@staff.com',
        password=password,
        is_staff=True,
    )
    get_user = User.objects.get(username=username)
    new_staff = Profile.objects.create(
                    user=get_user,
                    birthday='2001-01-01',
                    pfp="",
                    first_name='John',
                    last_name='Doe',
                    custom_slug_profile='example_slug'
                    )
    new_staff.save()
    url = reverse('api_get_auth_token')
    data = {'username': username, 'password': password}
    response_data = client.post(url, data=data)
    response_data_json = response_data.json()
    token = response_data_json['token']
    return token
    
    
@pytest.fixture
def create_multiple_users_with_profile(client, db):
    users_list = [
        {
            'username': 'john_doe',
            'email': 'john@doe.com',
            'password': 'johndoepassword',
            'birthday': '2001-01-01',
            'pfp': "",
            'first_name': 'John',
            'last_name': 'Doe',
            'custom_slug_profile': 'john_slug'          
        },
        {
            'username': 'jane_doe',
            'email': 'jane@doe.com',
            'password': 'janedoepassword',
            'birthday': '2001-01-01',
            'pfp': '',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'custom_slug_profile': 'jane_slug'
        }
    ]
    created_users = []
    for user in users_list:
        User.objects.create_user(
            username=user['username'], 
            email=user['email'], 
            password=user['password']
        )
        get_user = User.objects.get(username=user['username'])
        new_profile = Profile.objects.create(
            user= get_user,
            birthday=user['birthday'],
            pfp='',
            first_name=user['first_name'],
            last_name=user['last_name'],
            custom_slug_profile=user['custom_slug_profile']
        )
        new_profile.save()
        created_users.append(get_user)
    return created_users
    