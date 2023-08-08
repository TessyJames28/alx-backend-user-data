#!/usr/bin/env python3
"""Basic Authorization"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """class Basic Auth"""
    pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """return the Base64 part of the AUthorization header for Basic Auth"""
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str) is False:
            return None
        if authorization_header and authorization_header.startswith('Basic '):
            passwd = authorization_header[6:]
            return passwd
        else:
            return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # nopep8
        """
        returns the decoded value of a Base64 str base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if isinstance(base64_authorization_header, str) is False:
            return None
        try:
            val = base64.b64decode(base64_authorization_header)
            return val.decode('utf-8')
        except Exception:
            return None
