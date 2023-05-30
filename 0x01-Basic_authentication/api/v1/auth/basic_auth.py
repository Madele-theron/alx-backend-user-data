#!/usr/bin/env python3
"""
Module for basic authentication
"""
from typing import List, TypeVar
from flask import request
from auth import Auth


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
