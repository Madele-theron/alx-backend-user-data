#!/usr/bin/env python3
"""
Route module for the API auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manages API authentication
    """
    def __init__(self):
        """The construcotr"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication

        Args:
            path (str): path that needs to be authenticated
            excluded_paths (List[str]): excluded paths to authenticate

        Returns:
            True: if authenticated, else False
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        for paths in excluded_paths:
            if paths.endswith('*'):
                if path.startswith(paths[:-1]):
                    return False
            elif path == paths:
                return False
        return True


    def authorization_header(self, request=None) -> str:
        """Auth headers

        Args:
            request (_type_, optional): auth. Defaults to None.

        Returns:
            str: the auth header or None
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)


    def current_user(self, request=None) -> TypeVar('User'):
        """Current User

        Args:
            request: the request user

        Return:
            the authenticated user
        """
        return request
