#!/usr/bin/env python3
"""
session of authentication
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class to manage session authentication
    with sessions stored in the database."""

    def create_session(self, user_id=None):
        """Create and store a new session in the database."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID based on session ID by querying the database."""
        if session_id is None:
            return None

        try:
            user_sessions = UserSession.search({'session_id': session_id})
            if not user_sessions:
                return None

            user_session = user_sessions[0]
            if self.session_duration <= 0:
                return user_session.user_id

            created_at = user_session.created_at
            if created_at + \
                    timedelta(seconds=self.session_duration) < datetime.now():
                return None

            return user_session.user_id
        except Exception as e:
            return None

    def destroy_session(self, request=None):
        """Destroy the user session based on the session ID
        from the request cookie."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True
