#!/usr/bin/env python3
"""
This script contains the class that will implement
Basic authentication.
"""
from .auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ This method decode the base64 encoding. """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            b_decode = base64.standard_b64decode(base64_authorization_header)
            b_decode = b_decode.decode('utf-8')
            return b_decode
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """ This method splits the decode base64 code into
        username and password"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ":" in decoded_base64_authorization_header:
            values = decoded_base64_authorization_header.strip().split(':')
            return values[0].strip(), values[1]
        return None, None
