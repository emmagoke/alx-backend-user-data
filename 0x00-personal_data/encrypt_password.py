#!/usr/bin/env python3
"""
This script contains python functions that encrypt an data
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed password, which is a byte string """
    encoded_password = password.encode('utf-8')
    hashed = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed
