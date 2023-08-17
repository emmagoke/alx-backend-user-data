#!/usr/bin/env python3
"""
This is the Auth Module, it contains some function for authentication.
"""
import bcrypt
from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


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

    def create_session(self, email: str) -> str:
        """ This method creates a session id for a specific user. """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ This method gets user by their session id. """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user.session_id is None:
                return None
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ This method destory the the user session id
        by setting it to None. """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ This method generate and return the user's reset token. """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """ This method finds a user by reset_token and
        updates the users password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError()
