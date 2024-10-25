import requests
from config import ADMIN_API_BASE_URL

"""
auth.py

This module contains the function for authenticating with MongoDB Atlas using
public and private API keys.

Constants:
    ADMIN_API_BASE_URL (str): The base URL for the MongoDB Atlas Admin API.

Functions:
    authenticate(public_api_key, private_api_key): Authenticate with MongoDB Atlas and obtain an access token.
"""


def authenticate(public_api_key, private_api_key):
    """
    Authenticate with MongoDB Atlas using the provided public and private API keys.

    This function sends a POST request to the MongoDB Atlas authentication endpoint
    with the provided public and private API keys. If the authentication is successful,
    it returns the access token.

    Args:
        public_api_key (str): The public API key for MongoDB Atlas.
        private_api_key (str): The private API key for MongoDB Atlas.

    Returns:
        str: The access token obtained from MongoDB Atlas.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.exceptions.RequestException: For other types of request-related errors.
    """
    url = f"{ADMIN_API_BASE_URL}/auth/providers/mongodb-cloud/login"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"username": public_api_key, "apiKey": private_api_key}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["access_token"]
