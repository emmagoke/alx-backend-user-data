#!/usr/bin/env python3
"""
This script contains the class that will implement
Basic authentication.
"""
from .auth import Auth


class BasicAuth(Auth):
    """ Contains Basic Authentication Implementation. """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ This method returns the base64 encode string. """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header.split(' ')[0] != "Basic":
            return None
        return authorization_header.split(' ')[-1]
