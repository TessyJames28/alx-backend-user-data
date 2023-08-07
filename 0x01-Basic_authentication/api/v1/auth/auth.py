#!/usr/bin/env python3
"""The Auth Class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class name AUth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require path method"""
        return False

    def authorization_header(self, request=None) -> str:
        """authorization header method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user method"""
        return None
