#!/usr/bin/env python3
"""Session authentication module."""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Class for session authentication mechanism.

    It inherits from the Auth class and builds on-
    -the authentication methods in Auth.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Returns:
            - None if user_id is None.
            - None if user_id not a str.
            - Otherwise, generate Session ID w/ uuid.uuid4() like
            id in Base. Use the Session ID as key of dict called
            user_id_by_session_id; value of this key must be user_id.
            Return the Session ID.
        Same user_id can have multiple Session ID.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id
