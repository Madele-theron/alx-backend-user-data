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


def _generate_uuid() -> str:
    """ uuid generator """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method to register a new user with auth

        Args:
            email (str): user email
            password (str): user password

        Returns:
            User: Registered User
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists.")
        except NoResultFound:
            pswd = _hash_password(password=password)
            user = self._db.add_user(email, pswd)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Method to validate user login

        Args:
            email (str): email of user
            password (str): password of user

        Returns:
            bool: True if logins are valid, else False
        """
        try:
            user: User = self._db.find_user_by(email=email)
            valid: bool = bcrypt.checkpw(
                password=password.encode(),
                hashed_password=user.hashed_password)
        except NoResultFound:
            return False
        else:
            return valid

    def create_session(self, email: str) -> str:
        """Method to create a new session when user logs in

        Args:
            email (str): email of user

        Returns:
            str: id of session
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Method to get user based on session id

        Args:
            session_id (str):id of session

        Returns:
            str: User
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
