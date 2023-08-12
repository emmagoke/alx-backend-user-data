#!/usr/bin/env python3
"""
This script contains the class that will implement
Session authentication.
"""
from .auth import Auth
from uuid import uuid4


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
