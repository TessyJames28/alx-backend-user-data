#!/usr/bin/env python3
"""Hash password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hashed password"""
    salt = bcrypt.gensalt()
    hash_passwd = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash_passwd
