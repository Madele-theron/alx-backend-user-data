#!/usr/bin/env python3
"""
Module for basic authentication
"""
from typing import TypeVar
from models.user import User
from auth import Auth
from base64 import b64decode, binascii


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
            isinstance(authorization_header, str) or\
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
    if decode_base64_authorization_header is None or\
        not isinstance(decode_base64_authorization_header, str)\
            ":" not in decode_base64_authorization_header:
        return None, None
    user_cred = decode_base64_authorization_header.split(":", 1)
    return user_cred[0], user_cred[1]
