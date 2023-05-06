"""Test module for the ApiRequest class."""
import pytest

from config import settings


@pytest.fixture(scope='module')
def test_init():
    """Fixture to initialize the ApiRequest object."""
    from onequant.api.request import ApiRequest

    return ApiRequest(settings.api_url)


def test_login(test_init):
    """Test function to check the login functionality."""
    username = settings.username
    password = settings.password
    response = test_init.login(username, password)
    assert response and len(response) > 0, 'Login Response is empty'


def test_get_request(test_init):
    """Test function to check the get request functionality."""
    response = test_init.request(method='get', router='/system/user/get')
    assert response and response['success'], 'Get method request failed!'


def test_post_request(test_init):
    """Test function to check the post request functionality."""
    response = test_init.request(method='post', router='/system/login/outLogin')
    assert response and response['success'], 'Post method request failed!'


if __name__ == '__main__':
    pytest.main()
