#!/usr/bin/env python3
"""Hash password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hashed_password)  # nopep8
            return user
        raise ValueError("User {} already exists".format(email))
