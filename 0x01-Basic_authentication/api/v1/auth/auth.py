#!/usr/bin/env python3
"""
Route module for the API auth
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Manages API authentication
    """

    def __init__(self):
        """This is the constructor
        """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication

        Args:
            path (str): path that needs to be authenticated
            excluded_paths (List[str]): excluded paths to authenticate

        Returns:
            True: if authenticated, else False
        """


def authorization_header(self, request=None) -> str:
    """Auth headers

    Args:
        request (_type_, optional): auth. Defaults to None.

    Returns:
        str: the auth header or None
    """
    if request is None:
        return None
    return request.headers.get("Authorization", None)


def current_user(self, request=None) -> TypeVar('User'):
    """Current User

    Args:
        request: the request user

    Return:
        the authenticated user
    """
    return request
