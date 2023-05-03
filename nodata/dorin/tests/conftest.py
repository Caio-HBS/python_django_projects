import pytest

from django.contrib.auth.models import User

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
def post_data_for_register(client, db):
    """
        Fixture to provide data to POST method in the registe page.
    """
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'first-name': 'John',
        'last-name': 'Doe',
        'birthday': '01/01/1990',
        'slug': 'testuser1234567',
        'password': 'testpassword123',
        'confirm-password': 'testpassword123',
    }