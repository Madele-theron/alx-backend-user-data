#!/usr/bin/env python3
"""
Module for the class DB
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """ DB Class for the database """

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """ create session """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Method to create a new user

            Args:
                email: email of user
                hashed_password: hashed password

            Return:
                User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Method to find a user using keyword arguments

        Returns:
            User: User that was searched for
        """
        if kwargs is None:
            raise InvalidRequestError

        for key in kwargs.keys():
            if key not in User.__table__.columns.keys():
                raise InvalidRequestError

        user = self._session.query(User).filter_by(
                                                    **kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method that will find & update a user in the database

        Args:
            user_id (int): id of user that will be modified
        """
        if kwargs is None:
            return None

        user = self.find_user_by(id=user_id)
        for key in kwargs.keys():
            if key not in User.__table__.columns.keys():
                raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
