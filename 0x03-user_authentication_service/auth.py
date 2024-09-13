#!/usr/bin/env python3
"""Module for authentication methods."""
import bcrypt


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
