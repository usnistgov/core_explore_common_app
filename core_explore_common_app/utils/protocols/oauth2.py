""" oauth2 utils
"""
from core_explore_common_app.commons.exceptions import UsernamePasswordRequiredError
import requests

HEADER = {'content-type': 'application/x-www-form-urlencoded'}
TOKEN_SUFFIX = "/o/token/"


def post_request_token(url, client_id, client_secret, timeout, username, password):
    """ Request token

    Args:
        url:
        client_id:
        client_secret:
        timeout:
        username:
        password:

    Returns:

    """
    # Complete Url
    token_url = "{0}{1}".format(url, TOKEN_SUFFIX)

    data = _get_data_for_request(client_id, client_secret, username=username, password=password)

    return requests.post(url=token_url, data=data, headers=HEADER, timeout=int(timeout))


def post_refresh_token(url, client_id, client_secret, timeout, refresh_token):
    """ Refresh token

    Args:
        url:
        client_id:
        client_secret:
        timeout:
        refresh_token:

    Returns:

    """
    # Complete Url
    token_url = "{0}{1}".format(url, TOKEN_SUFFIX)

    data = _get_data_for_request(client_id, client_secret, refresh_token=refresh_token)

    return requests.post(url=token_url, data=data, headers=HEADER, timeout=int(timeout))


def _get_data_for_request(client_id, client_secret,
                          username=None, password=None, refresh_token=None):
    """ Returns data structure for post request

    Args:
        client_id:
        client_secret:
        username:
        password:
        refresh_token:

    Returns:

    """
    # Init data
    data = {
        'client_id': str(client_id),
        'client_secret': str(client_secret),
    }

    if refresh_token is not None:
        data.update({'refresh_token': str(refresh_token),
                     'grant_type': 'refresh_token'})
    else:
        if username is not None and password is not None:
            data.update({'grant_type': 'password',
                         'username': username,
                         'password': password})
        else:
            raise UsernamePasswordRequiredError("Username/Password must be given")

    return data
