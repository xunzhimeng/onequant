"""Api for connecting to trading server.

Basic function of fetching data from API server.
"""
import requests  # type: ignore


class ApiRequest:
    """Class for connecting to trading server.

    Basic function of fetching data from API server.
    """

    def __init__(self, url):
        """Initializes the ApiRequest class with a given url.

        Args:
            url (str): The url to be used for the API request.
        """
        self.url = url
        self.token = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    def login(self, username, password):
        """Logs in to the API with the given username and password.

        Args:
            username (str): The username to be used for the login.
            password (str): The password to be used for the login.

        Returns:
            str: The token for the logged in user.
        """
        data = {'username': username, 'password': password, 'autoLogin': False, 'type': 'pc'}

        response = requests.post(url=self.url + '/system/login/login', json=data, headers=self.headers)
        if 'Set-Cookie' in response.headers:
            import re

            match = re.search(r'satoken=([\w-]+);', response.headers['Set-Cookie'])
            if match:
                self.token = 'satoken=' + match.group(1)
                self.headers['Cookie'] = self.token

        return self.token

    def request(self, method, router, params=None, data=None, json=None):
        """Sends a request to the API with the given parameters.

        Args:
            method (str): The HTTP method to be used for the request.
            router (str): The router to be used for the request.
            params (dict, optional): The parameters to be used for the request. Defaults to None.
            data (dict, optional): The data to be used for the request. Defaults to None.
            json (dict, optional): The json to be used for the request. Defaults to None.

        Raises:
            AssertionError: If an unsupported request method is used.

        Returns:
            dict: The response from the API in json format.
        """
        assert method in ['get', 'post', 'put', 'delete'], 'Unsupported request method'

        response = requests.request(
            method=method, url=self.url + router, params=params, data=data, json=json, headers=self.headers
        )

        return response.json()


class ApiWrapper:
    """Wrapper for keep using ApiRequest."""

    def __init__(self, url, username, password):
        """Initializes the ApiWrapper class with a given url, username, and password.

        Args:
            url (str): The url to be used for the API request.
            username (str): The username to be used for the login.
            password (str): The password to be used for the login.
        """
        self.api = ApiRequest(url)
        self.api.login(username, password)
        self.username = username
