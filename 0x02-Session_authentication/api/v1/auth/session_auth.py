#!/usr/bin/env python3
"""
This script contains the class that will implement
Session authentication.
"""
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ Contains Session Authentication Implementation. """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ This session create the session id for the user """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ This method return the user_id based on the session_id """
        if type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ This method deletes the user session. """
        session_id = self.session_cookie(request)
        if request is None or session_id is None:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
