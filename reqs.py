import requests
import json

base_url = "http://e00m.duckdns.org/"
user_endpoint = "users/"
user_vaccines_endpoint = "users/doses/"
all_vaccines_endpoint = "vacs/"

def get_user_info(username: str, password: str) -> requests.Response:
    """Makes a request to the server using the username and password
    provided by the user and returns the user info"""

    login_response = requests.get(base_url + user_endpoint, auth=(username, password))
    return login_response


def get_user_vaccines(username: str, password: str) -> requests.Response:
    """Makes a request to the server using the username and password
    provided by the user and returns the user vaccines"""

    login_response = requests.get(base_url + user_vaccines_endpoint, auth=(username, password))
    return login_response


def get_all_vaccines() -> requests.Response:
    """Makes a request to the server using the username and password
    provided by the user and returns vaccines available"""

    login_response = requests.get(base_url + all_vaccines_endpoint)
    return login_response


def register_vac(user_info: tuple[str, str], vac_info: dict[str, str]) -> requests.Response:
    """Register the vaccine and its date according to the user input"""
    data = json.dumps(vac_info)
    register_vac_response = requests.post(base_url + user_vaccines_endpoint, auth=user_info, data=data)
    return register_vac_response


def register_user(user_info: dict[str, str]) -> requests.Response:
    """Makes a request to the server using the required data,
    provided by the user, and returns the response"""

    data = json.dumps(user_info)
    register_response = requests.post(base_url + user_endpoint, data=data)
    return register_response


def remove_user(username: str, password: str) -> requests.Response:
    """Deletes the user information given in the authentication data"""

    remove_response = requests.delete(base_url + user_endpoint, auth=(username, password))
    return remove_response


def update_password(username: str, password: str, new_password: str) -> requests.Response:
    """Updates the user information given in the authentication data"""

    data = {"password": new_password}
    data = json.dumps(data)
    update_response = requests.put(base_url + user_endpoint, auth=(username, password), data=data)
    return update_response
