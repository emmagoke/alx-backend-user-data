#!/usr/bin/env python3
"""
This is the Auth Module, it contains some function for authentication.
"""
import bcrypt
from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw."""
    encoded_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """ This function a string representation of a new UUID. """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ This is the constructor for this class """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ This method reigsters a user using the email and password. """
        if email and password:
            try:
                user = self._db.find_user_by(email=email)
                raise ValueError("User {} already exists".format(email))
            except NoResultFound:
                user = self._db.add_user(email, _hash_password(password))
                return user

    def valid_login(self, email: str, password: str) -> bool:
        """ This method check if the user details are correct """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                encoded_password = password.encode('utf-8')
                if bcrypt.checkpw(encoded_password, user.hashed_password):
                    return True
            return False
        except NoResultFound:
            return False
