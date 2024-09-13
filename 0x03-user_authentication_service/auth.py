#!/usr/bin/env python3
"""Module for authentication methods."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password, passed as an arg, using bcrypt module.

    Args:
        - password: the password string to hash.

    Returns:
        - bytes: salted hash of password str w/ bcrypt.hashpw.
    """
    encoded_password = password.encode('utf-8')

    salt = bcrypt.gensalt()
    salted_hash = bcrypt.hashpw(encoded_password, salt)

    return salted_hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user.

        Args:
            - email: the user's email.
            - password: the user's password.

        Returns:
            - User: the created User object.

        Raises:
            - ValueError: when user w/ provided email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_password = _hash_password(password)
            user = self._db.add_user(email, hash_password)
            return user
