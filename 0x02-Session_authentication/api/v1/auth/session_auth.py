#!/usr/bin/env python3
"""Session authentication module."""
from api.v1.auth.auth import Auth
from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Creates an instance method.

        Returns:
            - None if session_id is None.
            - None if session_id not a string.
            - value (user ID) for key, session_id in dict called
            user_id_by_session_id.
        Must use .get() built-in to access value w/ key in dict.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the User instance based on the session cookie.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout.
        """
        if request is None:
            return False
        
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        
        del self.user_id_by_session_id[session_id]
        return True
