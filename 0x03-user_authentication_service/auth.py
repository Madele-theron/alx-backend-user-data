#!/usr/bin/env python3
"""Module for the Auth class
"""
from uuid import uuid4
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Convert password to hashed password

    Args:
        password (str): password to be hashed

    Returns:
        str: hashed password
    """
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
