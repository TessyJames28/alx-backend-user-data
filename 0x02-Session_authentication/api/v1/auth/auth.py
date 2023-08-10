#!/usr/bin/env python3
"""The Auth Class"""
from flask import request
from typing import List, TypeVar
from os import environ


class Auth:
    """class name Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require path method"""
        slashed_path = None
        if path is not None and type(path) is str:
            if path[-1] == "/":
                slashed_path = path[:-1]
            else:
                slashed_path = path + "/"
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or slashed_path in excluded_paths:
            return False

        for paths in excluded_paths:
            if paths.endswith("*"):
                prefix = paths[:-1]
                if path.startswith(prefix):
                    return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """authorization header method"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """current user method"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        session_cookie = environ.get("SESSION_NAME", "_my_session_id")
        session_cookie_val = request.cookies.get(session_cookie)
        return session_cookie_val
