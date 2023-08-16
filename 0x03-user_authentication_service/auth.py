#!/usr/bin/env python3
"""
This is the Auth Module, it contains some function for authentication.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw."""
    encoded_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password
