#!/usr/bin/env python3
"""
This script contains the class that manage the API authentication.
"""
from flask import request
from typing import List, TypeVar
import re
from os import getenv


class Auth:
    """ manage the API authentication. """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ This method will be explain later """
        if path is None or excluded_paths is None:
            return True
        for item in excluded_paths:
            if item[-1] == '*':
                pattern = "{}.*".format(item[:-1])
                if re.match(pattern, path):
                    return False
            if path[-1] != '/':
                if path + '/' == item:
                    return False
            elif path == item:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ This method handles authorization headers"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ This method checks for the current user."""
        return None

    def session_cookie(self, request=None):
        """ This method request value of the cookie _my_session_id"""
        if request is None:
            return None
        session_id = getenv('SESSION_NAME')
        return request.cookies.get(session_id)
