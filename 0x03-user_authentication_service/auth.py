#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """hashed password"""
    salt = bcrypt.gensalt()
    hash_passwd = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash_passwd


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        locate user email, if exists check with bcrypt.checkpw
        return true if it matches else return false
        """
        try:
            user = self._db.find_user_by(email=email)
            passwd = password.encode('utf-8')
            if user:
                return bcrypt.checkpw(passwd, user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """returns the session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            user_update = self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User | None]:
        """Find user by session_id"""
        user = self._db.find_user_by(session_id=session_id)
        if not user:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy session method"""
        user = self._db.find_user_by(id=user_id)
        if user:
            self._db.update_user(user_id, session_id=None)
            return user.session_id

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token method"""
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password method"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_passwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hash_passwd, reset_token=None)  # nopep8
        except ValueError as e:
            raise e
