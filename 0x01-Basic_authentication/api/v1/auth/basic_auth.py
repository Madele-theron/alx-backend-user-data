#!/usr/bin/env python3
"""
Module for basic authentication
"""
from typing import TypeVar
from models.user import User
from base64 import b64decode, binascii
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Manages basic authentication
    """

    def __init__(self):
        """This is the constructor"""

    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str) -> str:
        """header extraction in base64

        Args:
            authorization_header (str): string in base64

        Returns:
            str: header in base64, else None
        """
        if authorization_header is None or\
            not isinstance(authorization_header, str) or\
                authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]


def decode_base64_authorization_header(
                                        self,
                                        base64_authorization_header: str
                                        ) -> str:
    """Decode base64

    Args:
        base64_authorization_header (str): heaeder in base64

    Returns:
        str: decoded header, else None
    """
    if base64_authorization_header is None or\
            not isinstance(base64_authorization_header, str):
        return None

    try:
        decode_header = b64decode(base64_authorization_header)
        return decode_header.decode('utf-8')
    except binascii.Error as error:
        return None


def extract_user_credentials(self,
                             decoded_base64_authorization_header: str
                             ) -> (str, str):
    """Returns User email and password
    """
    if decode_base64_authorization_header is None:
        return None, None
    if ":" not in decode_base64_authorization_header:
        return None, None
    if not isinstance(decode_base64_authorization_header, str):
        return None, None
    user_cred = decode_base64_authorization_header.split(":", 1)
    return user_cred[0], user_cred[1]


def user_object_from_credentials(self, user_email: str,
                                 user_pwd: str) -> TypeVar('User'):
    """
        Get user object from creds

        Args:
            user_email: Email
            user_pwd: password

        Return:
            The user, else None
    """
    if user_email is None or not isinstance(user_email, str):
        return None
    if user_pwd is None or not isinstance(user_pwd, str):
        return None
    try:
        users = User.search({'email': user_email})
    except Exception:
        return None

    for user in users:
        if user.is_valid_password(user_pwd):
            return user


def current_user(self, request=None) -> TypeVar('User'):
    """
        Get current user details

        Args:
            request: user

        Return:
            Detail of current user, else None
    """
    try:
        header: str = self.authorization_header(request)
        head64: str = self.extract_base64_authorization_header(header)
        auth_decode: str = self.decode_base64_authorization_header(head64)
        user_cred = self.extract_user_credentials(auth_decode)
        user = self.user_object_from_credentials(user_cred[0],
                                                 user_cred[1])
        return user
    except Exception:
        return None
