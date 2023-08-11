#!/usr/bin/env python3
"""Add expiration date to session"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """a class that adds expiration date to session ID"""
    user_id_by_session_id = {}
    session_dictionary = {}

    def __init__(self):
        """initialization"""
        try:
            self.session_duration = getenv(int('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session"""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            session_id = None
        if not session_id:
            return None
        self.session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        self.user_id_by_session_id[session_id] = self.session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user is for session id"""
        if session_id is None:
            return None
        if self.user_id_by_session_id.get(session_id) is None:
            return None
        if self.session_duration <= 0:
            return self.session_dictionary.get('user_id')
        if self.user_id_by_session_id.get('created_at') is None:
            return None
        created_at = session_data.get('created_at')
        current_time = datetime.datetime.now()
        exp_time = created_at + timedelta(seconds=self.session_duration)
        if current_time > exp_time:
            return None
        return session_dictionary.get('user_id')
