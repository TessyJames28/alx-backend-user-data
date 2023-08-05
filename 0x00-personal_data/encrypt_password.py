#!/usr/bin/env python3
"""Password encryption"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    salt = bcrypt.gensalt()
    hashpw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashpw
