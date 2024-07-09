"""
This module contains the main functions for the API Testing Toolkit

Functions:
    display(data) -> None
    display_response(response: Response, headers=False) -> None
    load_env(name: str) -> object
"""

from requests.structures import CaseInsensitiveDict
from requests.models import Response
from IPython.display import JSON, display as ipy_display
import json
from pathlib import Path


def display(data, label=None):
    """
    Display the data in a nice way, does not return anything but uses the IPython display function
    :param data: Some (mostly) JSON-able data
    :param label: Optional label to display
    :return: None
    """

    if isinstance(data, CaseInsensitiveDict):
        data = dict(data)  # just reset it

    if isinstance(data, dict) or isinstance(data, list):
        data = JSON(data, expanded=True)

    if label:
        print(label + ':')

    ipy_display(data)
    print('')  # add a new line


d = display  # alias for display


def display_response(response: Response, headers=False):
    """
    Helper function for displaying the response of JSON or text requests.

    Will parse JSON only if the content-type is json.
    :param response: The response object
    :param headers: Whether to display the headers
    :return: None
    """

    data_label = None

    if headers:
        data_label = 'Data'

    if not isinstance(response, Response):
        print('Not a Response object')
        return

    if 'json' in response.headers['content-type']:
        display(response.json(), data_label)
    else:
        display(response.text, data_label)

    if headers:
        display(response.headers, 'Headers')


dr = display_response  # alias for display_request


def load_env(name: str) -> object:
    """
    Load the environment variables from the env folder
    :param name: The name of the JSON document to load
    :return: The JSON object
    """

    try:
        f = open('env/{}.json'.format(name))
        return json.load(f)
    except FileNotFoundError:
        print('no env found, returning nothing')
        return {}


def save_env(data: object, name: str):
    """
    Save environment variables to the env folder
    :param data: The data to save to the environment
    :param name: The name of the JSON document to save
    :return: The JSON object
    """

    Path('env').mkdir(exist_ok=True)

    with open('env/{}.json'.format(name), 'w') as f:
        json.dump(data, f, indent=2)
