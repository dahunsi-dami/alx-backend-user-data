#!/usr/bin/env python3
"""SessionExpAuth implementation for session expiration."""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Class that implements session expiration authentication."""
    def __init__(self):
        """Initialize the SessionExpAuth instance."""
        super().__init__()
        try:
            self.session_duration = int(os.environ.get("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID with expiration."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID based on-
        -the session ID with expiration check.
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict["user_id"]

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_dict["user_id"]
