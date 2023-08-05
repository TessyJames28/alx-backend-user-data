#!/usr/bin/env python3
"""Password encryption"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    salt = bcrypt.gensalt()
    hashpw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashpw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check valid password"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False
