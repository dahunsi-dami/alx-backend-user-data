#!/usr/bin/env python3
"""A UserSession model for storing session data."""

from models.base import Base
from datetime import datetime
import uuid


class UserSession(Base):
    """The UserSession model for storing session-related data."""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize UserSession instance with session ID & user ID."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id", str(uuid.uuid4()))
        self.created_at = datetime.utcnow()
