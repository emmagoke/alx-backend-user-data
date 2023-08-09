#!/usr/bin/env python3
"""
This script contains the class that will implement
Basic authentication.
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


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
        except (base64.binascii.Error, UnicodeDecodeError):
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

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ This method return the authenicated user.  """
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) == str and type(user_email) == str:
            try:
                user_obj = User.search({"email": user_email})
            except Exception:
                return None
            if len(user_obj) <= 0:
                return None
            if user_obj[0].is_valid_password(user_pwd):
                return user_obj[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ This method gets the current user from the request."""

        header = self.authorization_header(request)
        encoded_header = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(
            encoded_header)
        email, password = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(email, password)
