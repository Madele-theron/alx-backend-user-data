#!/usr/bin/env python3
"""
Module for basic authentication
"""
from typing import List, TypeVar
from flask import request
from auth import Auth


class BasicAuth(Auth):
    """Manages API authentication
    """
