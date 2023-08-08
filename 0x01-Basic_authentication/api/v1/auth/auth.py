#!/usr/bin/env python3
"""
This script contains the class that manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ manage the API authentication. """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ This method will be explain later """
        if path is None or excluded_paths is None:
            return True
        for item in excluded_paths:
            if path[-1] != '/':
                if path + '/' == item:
                    return False
            elif path == item:
                return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """ This method handles authorization headers"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ This method checks for the current user."""
        return None
