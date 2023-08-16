import pytest
import random

from django.urls import reverse


def test_profile_list_view_full_list(
        client, 
        staff_user_token_retrieve, 
        create_multiple_users_with_profile
) -> None:
    """
        Tests the ProfileListAPIView enpoint with staff level clearance.

            Args:
                client: standard client provided by pytest-django.
                staff_user_token_retrieve: creates a new staff user and retrieves
                their token.
                create_multiple_users_with_profile: creates multiple users to
                make sure the query will be greater than just the created staff.
    """
    headers = {'Authorization': f"Bearer {staff_user_token_retrieve}"}
    response = client.get(reverse('api_profile_index'), headers=headers)
    
    assert response.status_code == 200
    assert response.json()['count'] == 3
    

def test_profile_list_view_own_profile(
        client,
        normal_user_token_retrieve,
        create_multiple_users_with_profile
) -> None:
    """
        Tests the ProfileListAPIView endpoint with basic user clearance.

            Args:
                client: standard client provided by pytest-django.
                normal_user_token_retrieve: creates a new user and retrieves
                their token.
                create_multiple_users_with_profile: creates multiple users to
                make sure the query will be greater than just the created staff.
    """
    headers = {'Authorization': f"Bearer {normal_user_token_retrieve}"}
    response = client.get(reverse('api_profile_index'), headers=headers)
    
    assert response.status_code == 200
    assert response.json()['count'] == 1


def test_profile_detail_authorized(
        client,
        staff_user_token_retrieve,
        create_multiple_users_with_profile
) -> None:
    """
        Tests the ProfileDetailAPIView endpoint with staff-level clearance.

            Args:
                client: standard client provided by pytest-django.
                staff_user_token_retrieve: creates a new staff user and retrieves
                their token.
                create_multiple_users_with_profile: creates multiple users to
                make sure the query will be greater than just the created staff.
    """
    headers = {'Authorization': f"Bearer {staff_user_token_retrieve}"}
    response = client.get(
        reverse(
        'api_profile_detail', 
        kwargs={'pk': random.choice([1, 2])}), 
        headers=headers
    )
    
    assert response.status_code == 200
    assert response.json()['user'] != "admin"


def test_profile_detail_unauthorized(
        client,
        normal_user_token_retrieve,
        create_multiple_users_with_profile
) -> None:
    """
        Tests the ProfileDetailAPIView endpoint without proper clearance.

            Args:
                client: standard client provided by pytest-django.
                normal_user_token_retrieve: creates a new user and retrieves
                their token.
                create_multiple_users_with_profile: creates multiple users to
                make sure the query will be greater than just the created staff.
    """
    headers = {'Authorization': f"Bearer {normal_user_token_retrieve}"}
    response = client.get(
        reverse('api_profile_detail', kwargs={'pk': random.choice([2, 3])}), 
        headers=headers
    )
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Not found."


def test_profile_update_view_authorized(
        client,
        staff_user_token_retrieve,
        create_multiple_users_with_profile
) -> None:
    """
        Tests the ProfileUpdateAPIView endpoint with proper clearance.

            Args:
                client: standard client provided by pytest-django.
                staff_user_token_retrieve: creates a new staff user and retrieves
                their token.
                create_multiple_users_with_profile: creates multiple users to
                make sure the query will be greater than just the created staff.
    """
    headers = {'Authorization': f"Bearer {staff_user_token_retrieve}"}
    data = {
        "first_name": "Name",
    }
    response = client.patch(reverse('api_profile_update', kwargs={'pk': 1}), 
        headers=headers, 
        data=data,
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert response.json()['first_name'] == 'Name'
    


def test_profile_update_view_unauthorized(
        client,
        normal_user_token_retrieve,
        create_multiple_users_with_profile
) -> None:
    """
        Tests the ProfileUpdateAPIView endpoint without proper clearance

            Args:
                client: standard client provided by pytest-django.
                normal_user_token_retrieve: creates a new user and retrieves
                their token.
                create_multiple_users_with_profile: creates multiple users to
                make sure the query will be greater than just the created staff.
    """
    headers = {'Authorization': f"Bearer {normal_user_token_retrieve}"}
    data = {
        "first_name": "Name",
    }
    response = client.patch(reverse('api_profile_update', kwargs={'pk': 2}), 
        headers=headers, 
        data=data,
        content_type='application/json'
    )
    
    assert response.status_code == 403
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_profile_destroy_view_authorized(
        client,
        staff_user_token_retrieve,
        create_multiple_users_with_profile) -> None:
    """
        Tests the ProfileDestroyAPIView endpoint with proper clearance.

            Args:
                client: standard client provided by pytest-django.
                staff_user_token_retrieve: creates a new staff user and retrieves
                their token.
                create_multiple_users_with_profile: creates multiple users to
                make sure the query will be greater than just the created staff.
    """
    headers = {'Authorization': f"Bearer {staff_user_token_retrieve}"}
    response = client.delete(
        reverse('api_profile_delete', kwargs={'pk': 1}),
        headers=headers, 
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json()['message'] == 'Profile deleted successfully'
    



def test_profile_destroy_view_unauthorized(
        client,
        normal_user_token_retrieve,
        create_multiple_users_with_profile
) -> None:
    """
        Tests the ProfileDestroyAPIView endpoint without proper clearance.

            Args:
                client: standard client provided by pytest-django.
                normal_user_token_retrieve: creates a new user and retrieves
                their token.
                create_multiple_users_with_profile: creates multiple users to
                make sure the query will be greater than just the created staff.
    """
    headers = {'Authorization': f"Bearer {normal_user_token_retrieve}"}
    response = client.delete(
        reverse('api_profile_delete', kwargs={'pk': 2}),
        headers=headers, 
        content_type='application/json'
    )
    
    assert response.status_code == 403
    assert response.json()['detail'] == 'You do not have permission to perform this action.'


def test_post_list_view_create_new_post(
        client, 
        staff_user_token_retrieve, 
        create_posts_data
) -> None:
    """
        Tests the PostListCreateAPIView by creating a new post.

            Args:
                client: standard client provided by pytest-django.
                staff_user_token_retrieve: creates a new staff user and retrieves
                their token.
                create_posts_data: provides data for the creation of posts
    """
    headers = {'Authorization': f"Bearer {staff_user_token_retrieve}"}
    data = create_posts_data
    data['post_slug'] = 'test-post'
    response = client.post(
        reverse('api_post_list_create', kwargs={'pk': 1}), 
        headers=headers, 
        data=data,
        content_type='application/json'
    
    )
    
    assert response.status_code == 201
    assert response.json()['post_text'] == 'This is a test for the post text'
    


def test_post_list_view_retrieve_posts_authorized(
        client, 
        staff_user_token_retrieve, 
        create_posts_data
) -> None:
    """
        Tests the PostListCreateAPIView by retrieving posts from own profile.

            Args:
                client: standard client provided by pytest-django.
    """
    headers = {'Authorization': f"Bearer {staff_user_token_retrieve}"}
    data = create_posts_data
    data['post_slug'] = 'test-post'
    new_post = client.post(
        reverse('api_post_list_create', kwargs={'pk': 1}), 
        headers=headers, 
        data=data,
        content_type='application/json'
    )
    response = client.get(
        reverse('api_post_list_create', kwargs={'pk': 1}), 
        headers=headers, 
        )

    assert response.status_code == 200
    assert response.json()['count'] > 0


def test_post_list_view_retrieve_posts_unauthorized(
        client, 
        staff_user_token_retrieve, 
) -> None:
    """
        Tests the PostListCreateAPIView by retrieving posts from a profile that
        it doesn't have clearance to.

            Args:
                client: standard client provided by pytest-django.
    """
    headers = {'Authorization': f"Bearer {staff_user_token_retrieve}"}
    response = client.get(
        reverse('api_post_list_create', kwargs={'pk': 1}), 
        headers=headers, 
        )

    assert response.status_code == 200
    assert response.json()['count'] == 0
