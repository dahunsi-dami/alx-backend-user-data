#!/usr/bin/env python3
"""Session-based auth module w/ session data stored in database."""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
import os


class SessionDBAuth(SessionExpAuth):
    """Session-based auth using database persistence for sessions."""

    def create_session(self, user_id=None):
        """Create and persist a session in the database."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id from session_id by querying database."""
        if session_id is None:
            return None

        try:
            user_sessions = UserSession.search({"session_id": session_id})
            if not user_sessions:
                return None

            user_session = user_sessions[0]

            session_duration = int(os.getenv("SESSION_DURATION", 0))
            if user_session.created_at + timedelta(
                seconds=session_duration
            ) < datetime.utcnow():
                user_session.remove()
                return None

            return user_session.user_id
        except KeyError:
            return None
        except Exception as e:
            return None

    def destroy_session(self, request=None):
        """Destroy the session by deleting it from the database."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False

        user_sessions[0].remove()
        return True
