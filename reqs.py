import requests
import json

base_url = "http://e00m.duckdns.org/"
user_endpoint = "users/"


def get_user_info(username: str, password: str) -> requests.Response:
    """Makes a request to the server using the username and password
    provided by the user and returns the response"""

    login_response = requests.get(base_url + user_endpoint, auth=(username, password))
    return login_response


def register_user(user_info: dict[str, str]) -> requests.Response:
    """Makes a request to the server using the required data,
    provided by the user, and returns the response"""

    data = json.dumps(user_info)
    register_response = requests.post(base_url + user_endpoint, data=data)
    return register_response
