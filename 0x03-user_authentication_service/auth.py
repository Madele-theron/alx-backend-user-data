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

    def destroy_session(self, user_id: str) -> None:
        """Method to destroy current session

        Args:
            user_id (str): id of user
        """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Method for user to reset password

        Args:
            email (str): email of user

        Returns:
            str: password token
        """
        if email is None:
            raise ValueError

        try:
            user = self._db.find_user_by(email=email)
            token: str = _generate_uuid()
            self._db.update_user((user.id), reset_token=token)
            return token

        except NoResultFound:
            raise ValueError

    # def update_password(self, reset_token: str, password: str) -> None:
    #     """Method to update the user password

    #     Args:
    #         reset_token (str): token to reset password
    #         password (str): users password
    #     """
    #     if reset_token is None or password is None:
    #         return None

    #     try:
    #         user = self._db.find_user_by(reset_token=reset_token)
    #     except NoResultFound:
    #         raise ValueError

    #     pswd = _hash_password(password)

    #     self._db.update_user(
    #         (user.id), hashed_password=pswd,
    #         reset_token=None)
