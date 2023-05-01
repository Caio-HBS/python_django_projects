import pytest


def test_index_redirect_with_user_should_succed(client, user_logged_in) -> None:
    response = client.get('/dorin/')
    assert response.status_code == 302
    assert response.url == '/dorin/feed/'


def test_index_redirect_no_user_should_succed(client) -> None:
    response = client.get('/dorin/')
    assert response.status_code == 302
    assert response.url == '/dorin/login/'


def test_login_redirect_with_user_should_succed(client, user_logged_in) -> None:
    response = client.get('/dorin/login/')
    assert response.status_code == 302
    assert response.url == '/dorin/feed/'


def test_login_redirect_no_user_should_succed(client) -> None:
    response = client.get('/dorin/login/')
    assert response.status_code == 200


def test_feed_redirect_with_user_should_succed(client, user_logged_in) -> None:
    response = client.get('/dorin/')
    assert response.status_code == 302
    assert response.url == '/dorin/feed/'


def test_feed_redirect_no_user_should_succed(client) -> None:
    response = client.get('/dorin/feed/')
    assert response.status_code == 302
    assert response.url == '/dorin/login/?next=/dorin/feed/'