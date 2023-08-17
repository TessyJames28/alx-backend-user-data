#!/usr/bin/env python3
"""Hash password"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hashed password"""
    salt = bcrypt.gensalt()
    hash_passwd = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash_passwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """return a User object"""
        user = User(email=email, hashed_password=password)
        if user.email:
            raise ValueError("User {} already exists".format(user.email))
        else:
            hash = _hash_password(user.password)
            self._db._session.add(user)
        return user
